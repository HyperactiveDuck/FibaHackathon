import { Anthropic } from "@anthropic-ai/sdk";
import {
  MessageParam,
  Tool,
} from "@anthropic-ai/sdk/resources/messages/messages.mjs";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import readline from "readline/promises";
import dotenv from "dotenv";

import express from "express";
import type { RequestHandler } from "express";
import cors from "cors";
import { error } from "console";

dotenv.config();

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
if (!ANTHROPIC_API_KEY) {
  throw new Error("ANTHROPIC_API_KEY is not set");
}

class MCPClient {
  private mcp: Client;
  private anthropic: Anthropic;
  private transport: StdioClientTransport | null = null;
  private tools: Tool[] = [];

  getTools(){
    return this.tools;
  }

  constructor() {
    this.anthropic = new Anthropic({
      apiKey: ANTHROPIC_API_KEY,
    });
    this.mcp = new Client({ name: "mcp-client-cli", version: "1.0.0" });
  }
  // methods will go here
  async connectToServer(serverScriptPath: string) {
  try {
    const isJs = serverScriptPath.endsWith(".js");
    const isPy = serverScriptPath.endsWith(".py");
    if (!isJs && !isPy) {
      throw new Error("Server script must be a .js or .py file");
    }
    const command = isPy
      ? process.platform === "win32"
        ? "py -3.12"
        : "python3.12"
      : process.execPath;

    this.transport = new StdioClientTransport({
      command,
      args: [serverScriptPath],
    });
    await this.mcp.connect(this.transport);

    const toolsResult = await this.mcp.listTools();
    this.tools = toolsResult.tools.map((tool) => {
      return {
        name: tool.name,
        description: tool.description,
        input_schema: tool.inputSchema,
      };
    });
    console.log(
      "Connected to server with tools:",
      this.tools.map(({ name }) => name)
    );
  } catch (e) {
    console.log("Failed to connect to MCP server: ", e);
    throw e;
  }
}
async processQuery(query: string) {
  const messages: MessageParam[] = [
    {
      role: "user",
      content: query,
    },
  ];

  const response = await this.anthropic.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 7000,
    messages,
    tools: this.tools,
  });

  const finalText = [];

  for (const content of response.content) {
    if (content.type === "text") {
      finalText.push(content.text);
    } else if (content.type === "tool_use") {
      const toolName = content.name;
      const toolArgs = content.input as { [x: string]: unknown } | undefined;

      console.log(`Calling tool: ${toolName} with args:`, toolArgs);

      const result = await this.mcp.callTool({
        name: toolName,
        arguments: toolArgs,
      });

      console.log(`Tool result:`, result);

      // Add the assistant's tool use message
      messages.push({
        role: "assistant",
        content: [content]
      });

      // Add the tool result
      messages.push({
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: content.id,
            content: typeof result.content === 'string' ? result.content : JSON.stringify(result.content)
          }
        ]
      });

      // Get Claude's response to the tool result
      const followUpResponse = await this.anthropic.messages.create({
        model: "claude-3-5-sonnet-20241022",
        max_tokens: 2000,
        messages,
        tools: this.tools,
      });

      // Add the follow-up response
      for (const followUpContent of followUpResponse.content) {
        if (followUpContent.type === "text") {
          finalText.push(followUpContent.text);
        }
      }
    }
  }

  return finalText.join("\n");
}

async cleanup() {
  await this.mcp.close();
}
}
async function main() {
  if (process.argv.length < 3) {
    console.log("Usage: node index.ts <path_to_server_script>");
    return;
  }

  const app = express()
  const port = process.env.PORT || 3000;

  app.use(cors());
  app.use(express.json());

  const mcpClient = new MCPClient();

  try{
    await mcpClient.connectToServer(process.argv[2]);

    const healthCheck: RequestHandler = (req, res) => {
      res.json({status: 'ok', tools: mcpClient.getTools().map(t => t.name)});
    }
    app.get('/health',healthCheck);

    //Query
    const chatHandler: RequestHandler = async (req,res) =>{
      try{
        const {query} = req.body;
        if(!query){
          res.status(400).json({error: "Query can't be empty"});
          return;
        }

        const response = await mcpClient.processQuery(query);
        res.json({response});
      }catch(error){
        console.error("Error in query process: ",error);
        res.status(500).json({error: "Failed to process query"});
      }
    };
    app.post('/chat',chatHandler);

    const server = app.listen(port, ()=>{
      console.log(`Server listening on port ${port}`);
      console.log(`Health check: http://localhost:${port}/health`);
      console.log(`Chat endpoint: POST http://localhost:${port}/chat`);
    });

    // Cleanup on exit
    process.on('SIGINT', async () => {
      console.log('\nShutting down gracefully...');
      await mcpClient.cleanup();
      server.close();
      process.exit(0);
    });

  }catch (error){
    console.error("Failed to start server: ",error);
    process.exit(1);
  }
}

main();