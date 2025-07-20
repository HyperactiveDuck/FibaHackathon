# MCP Client TypeScript

A TypeScript client for interacting with Model Context Protocol (MCP) servers through Claude AI. This project provides both a CLI interface and an HTTP API server for processing queries using MCP tools.

## Overview

This client connects to MCP servers, discovers available tools, and uses Claude AI to process user queries with those tools. It supports both Python and JavaScript MCP servers and provides a REST API for integration with other applications.

## Features

- 🔧 **MCP Server Integration**: Connect to Python (.py) or JavaScript (.js) MCP servers
- 🤖 **Claude AI Integration**: Uses Claude 3.5 Sonnet for intelligent query processing
- 🌐 **HTTP API**: RESTful endpoints for chat and health checks
- 🛠️ **Tool Discovery**: Automatically discovers and uses available MCP tools
- ⚡ **TypeScript**: Full TypeScript support with type safety
- 🔄 **CORS Support**: Cross-origin requests enabled for web integration

## Prerequisites

- Node.js (v18 or higher)
- TypeScript
- Python 3.12 (if using Python MCP servers)
- Anthropic API key

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd mcp-client-typescript
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   PORT=3000
   ```

4. **Build the project**:
   ```bash
   npm run build
   ```

## Usage

### Starting the Server

Run the application with a path to your MCP server script:

```bash
node build/index.js <path_to_server_script>
```

**Examples:**
```bash
# For a Python MCP server
node build/index.js ./servers/my-python-server.py

# For a JavaScript MCP server
node build/index.js ./servers/my-js-server.js
```

### API Endpoints

Once the server is running, you can interact with it through the following endpoints:

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "tools": ["tool1", "tool2", "tool3"]
}
```

#### Chat/Query Processing
```http
POST /chat
Content-Type: application/json

{
  "query": "Your question or request here"
}
```

**Response:**
```json
{
  "response": "Claude's response using MCP tools"
}
```

### Example Usage

```bash
# Start the server
node build/index.js ./my-mcp-server.py

# In another terminal, test the API
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What tools are available?"}'
```

## Development

### Scripts

- `npm run build`: Compile TypeScript to JavaScript
- `npm test`: Run tests (currently not implemented)

### Project Structure

```
mcp-client-typescript/
├── index.ts          # Main application file
├── package.json      # Dependencies and scripts
├── tsconfig.json     # TypeScript configuration
├── build/            # Compiled JavaScript output
│   └── index.js
└── README.md         # This file
```

### Building from Source

1. Make changes to `index.ts`
2. Rebuild the project:
   ```bash
   npm run build
   ```
3. Run the updated version:
   ```bash
   node build/index.js <server_path>
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (required) | - |
| `PORT` | Port for the HTTP server | 3000 |

### TypeScript Configuration

The project uses the following TypeScript configuration:
- Target: ES2022
- Module: Node16
- Strict mode enabled
- Output directory: `./build`

## Dependencies

### Production Dependencies
- `@anthropic-ai/sdk`: Claude AI integration
- `@modelcontextprotocol/sdk`: MCP protocol implementation
- `express`: HTTP server framework
- `cors`: Cross-origin resource sharing
- `dotenv`: Environment variable management

### Development Dependencies
- `typescript`: TypeScript compiler
- `@types/node`: Node.js type definitions
- `@types/express`: Express type definitions
- `@types/cors`: CORS type definitions

## Error Handling

The application includes comprehensive error handling:
- Missing API key validation
- Server connection failures
- Invalid query processing
- Graceful shutdown on SIGINT

## Platform Support

- **Windows**: Uses `py -3.12` for Python servers
- **Unix/Linux/macOS**: Uses `python3.12` for Python servers
- **JavaScript servers**: Uses Node.js on all platforms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Build and test
5. Submit a pull request

## License


## Troubleshooting

### Common Issues

1. **Missing ANTHROPIC_API_KEY**: Ensure your `.env` file contains a valid API key
2. **Python server not found**: Make sure Python 3.12 is installed and accessible
3. **Port already in use**: Change the PORT environment variable or stop other services using port 3000
4. **MCP server connection fails**: Verify the server script path and that the server is compatible with MCP

### Getting Help

- Check the console output for detailed error messages
- Ensure all dependencies are installed with `npm install`
- Verify your MCP server is working independently
- Test the API endpoints with curl or a REST client

## Related Projects

- [Model Context Protocol](https://github.com/modelcontextprotocol)
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-typescript)

This readme was prepared with help from Claude Sonnet 4