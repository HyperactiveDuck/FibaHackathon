import sqlite3
import random

# Connect to your SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # Update all rows to set user_id = 2
    cursor.execute("UPDATE finance_transaction SET user_id = ?", (2,))
    print(f"Updated user_id for {cursor.rowcount} rows")
    
    # Define the account_id options
    account_ids = [1, 2, 11, 12, 13, 14]
    
    # Get all transaction IDs
    cursor.execute("SELECT transaction_id FROM finance_transaction")
    transaction_ids = [row[0] for row in cursor.fetchall()]
    
    # Update each transaction with a random account_id from the list
    for trans_id in transaction_ids:
        random_account_id = random.choice(account_ids)
        cursor.execute("UPDATE finance_transaction SET account_id = ? WHERE transaction_id = ?", 
                      (random_account_id, trans_id))
    
    print(f"Updated account_id for {len(transaction_ids)} transactions")
    
    # Commit the changes
    conn.commit()
    
    # Verify the update
    cursor.execute("SELECT account_id, COUNT(*) FROM finance_transaction GROUP BY account_id ORDER BY account_id")
    results = cursor.fetchall()
    print("\nAccount ID distribution:")
    for account_id, count in results:
        print(f"Account ID {account_id}: {count} transactions")
    
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    conn.rollback()
    
finally:
    conn.close()