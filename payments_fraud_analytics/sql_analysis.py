import sqlite3
import pandas as pd

# 1. Connecting to SQLite-creating database
conn = sqlite3.connect('paytm_payments.db')
cursor = conn.cursor()

# 2. Defining Normalized Schema
cursor.executescript('''
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS merchants;

    CREATE TABLE merchants (
        merchant_id INTEGER PRIMARY KEY,
        merchant_name TEXT,
        category TEXT,
        region TEXT
    );

    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        signup_date TEXT
    );

    CREATE TABLE transactions (
        transaction_id TEXT PRIMARY KEY,
        user_id INTEGER,
        merchant_id INTEGER,
        transaction_time TEXT,
        amount_inr REAL,
        payment_method TEXT,
        status TEXT,
        risk_score INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (merchant_id) REFERENCES merchants (merchant_id)
    );
''')

# 3. Loading CSV data into the database
merchants_df = pd.read_csv('merchants.csv')
users_df = pd.read_csv('users.csv')
ledger_df = pd.read_csv('ledger.csv')

merchants_df.to_sql('merchants', conn, if_exists='append', index=False)
users_df.to_sql('users', conn, if_exists='append', index=False)
ledger_df.to_sql('transactions', conn, if_exists='append', index=False)

print("Database 'paytm_payments.db' created and populated successfully!\n" + "="*60)

# 4. 6 SQL queries
queries = {
    "Query 1: Quantify Chargeback Impact (Aggregation)": """
        SELECT 
            COUNT(transaction_id) AS chargeback_count,
            COUNT(DISTINCT user_id) AS unique_users_affected,
            SUM(amount_inr) AS total_chargeback_amount
        FROM transactions
        WHERE status = 'chargeback';
    """,
    
    "Query 2: Identify Burner Accounts (Strict 0-30 days logic)": """
        SELECT 
            t.transaction_id, 
            t.user_id, 
            t.amount_inr, 
            u.signup_date, 
            t.transaction_time,
            CAST(julianday(t.transaction_time) - julianday(u.signup_date) AS INTEGER) AS account_age_days
        FROM transactions t
        INNER JOIN users u ON t.user_id = u.user_id
        WHERE t.status = 'chargeback' 
          AND (julianday(t.transaction_time) - julianday(u.signup_date)) >= 0
          AND (julianday(t.transaction_time) - julianday(u.signup_date)) < 30;
    """,
    
    "Query 3: Detect Velocity Attacks (>=3 txns in 10-min window)": """
        SELECT 
            user_id,
            substr(transaction_time, 1, 15) || '0' AS time_bucket,
            COUNT(transaction_id) AS txn_count,
            SUM(amount_inr) AS total_amount
        FROM transactions
        GROUP BY user_id, time_bucket
        HAVING COUNT(transaction_id) >= 3
        ORDER BY txn_count DESC;
    """,

    "Query 4: General SELECT/WHERE/ORDER BY/LIMIT": """
        SELECT transaction_id, user_id, amount_inr, payment_method, risk_score
        FROM transactions
        WHERE status = 'captured' AND amount_inr > 2000
        ORDER BY risk_score DESC
        LIMIT 5;
    """,

    "Query 5: INNER JOIN with DISTINCT (High-Risk Categories)": """
        SELECT DISTINCT m.category, m.region
        FROM transactions t
        INNER JOIN merchants m ON t.merchant_id = m.merchant_id
        WHERE t.risk_score >= 95;
    """,

    "Query 6: LEFT JOIN + GROUP BY (Merchant Revenue Summary)": """
        SELECT 
            m.merchant_name, 
            COUNT(t.transaction_id) AS total_txns,
            SUM(t.amount_inr) AS total_revenue
        FROM merchants m
        LEFT JOIN transactions t ON m.merchant_id = t.merchant_id
        GROUP BY m.merchant_name
        ORDER BY total_revenue DESC
        LIMIT 5;
    """
}

# 5. Execution
for title, sql in queries.items():
    print(f"\n{title}")
    print("-" * len(title))
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False))

conn.close()