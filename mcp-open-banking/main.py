from typing import *

import httpx
from mcp.server.fastmcp import FastMCP
import csv
import os
import sys

class Transaction(TypedDict):
    transaction_id: str
    account_id: str
    amount: float
    currency: Optional[str]
    date: str
    description: Optional[str]

# Initialize FastMCP server
mcp = FastMCP("openbank")


@mcp.tool()
def get_transactions(description: Optional[str] = None) -> List[Transaction]:
    """
    Retrieve transactions from the CSV file.

    Args:
        description: If provided, only transactions whose description contains this substring (case-insensitive).

    Returns:
        A list of transactions matching the optional filter.
    """
    # Determine possible file locations
    ####
    base_dir = os.path.dirname(__file__)
    cwd = os.getcwd()
    possible = [
        os.path.join(base_dir, "transactions.csv"),
        os.path.join(cwd, "transactions.csv"),
    ]
    for path in possible:
        if os.path.exists(path):
            transactions_file = path
            break
    else:
        print(f"Error: transactions.csv not found. Searched: {possible}", file=sys.stderr)
        raise FileNotFoundError(f"transactions.csv not found in {possible}")
    ##### Bu blok sqlite db üzerinden veri çekecek şekilde güncellenmeli

    results: List[Transaction] = []

    # Open file with explicit encoding, replacing invalid chars
    try:
        csvfile = open(transactions_file, newline="", encoding="utf-8-sig", errors="replace")
    except (UnicodeError, LookupError):
        csvfile = open(transactions_file, newline="", encoding=sys.getdefaultencoding(), errors="replace")
    ### ENCODING BLOCK


    with csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Filter by description substring if specified
            desc = row.get("description", "") or ""
            if description and description.lower() not in desc.lower():
                continue

            # Parse amount as float
            try:
                amount_val = float(row.get("amount", 0))
            except (ValueError, TypeError):
                amount_val = 0.0

            # Build transaction record
            txn: Transaction = {
                "transaction_id": row.get("transaction_id", ""),
                "account_id": row.get("account_id", ""),
                "amount": amount_val,
                "currency": row.get("currency"),
                "date": row.get("date", ""),
                "description": desc,
            }
            results.append(txn)

    return results

if __name__ == "__main__":
     mcp.run(transport='stdio')