import pandas as pd
import mysql.connector
from mysql.connector import Error

CSV_PATH = r"C:\Users\Amit\Project 4\indian_banking_transactions.csv"

try:
    print("Reading CSV...")
    df = pd.read_csv(CSV_PATH)

    print(f"Rows found: {len(df):,}")
    print(f"Columns found: {len(df.columns)}")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=input("Enter MySQL password: "),
        database="finsight_india"
    )

    cursor = connection.cursor()

    print("Connected to MySQL.")

    # Remove incomplete previous import
    cursor.execute("DROP TABLE IF EXISTS raw_transactions")

    cursor.execute("""
        CREATE TABLE raw_transactions (
            transaction_id VARCHAR(50),
            customer_id VARCHAR(50),
            transaction_date DATE,
            transaction_time TIME,
            account_type VARCHAR(50),
            transaction_type VARCHAR(100),
            transaction_amount DECIMAL(15,2),
            transaction_direction VARCHAR(20),
            account_balance DECIMAL(15,2),
            merchant_category VARCHAR(100),
            state VARCHAR(100),
            credit_score INT,
            has_loan TINYINT,
            loan_type VARCHAR(100),
            emi_amount DECIMAL(15,2),
            transaction_status VARCHAR(50),
            channel VARCHAR(50),
            kyc_status VARCHAR(50),
            is_fraud TINYINT,
            transaction_hour TINYINT
        )
    """)

    insert_sql = """
        INSERT INTO raw_transactions (
            transaction_id,
            customer_id,
            transaction_date,
            transaction_time,
            account_type,
            transaction_type,
            transaction_amount,
            transaction_direction,
            account_balance,
            merchant_category,
            state,
            credit_score,
            has_loan,
            loan_type,
            emi_amount,
            transaction_status,
            channel,
            kyc_status,
            is_fraud,
            transaction_hour
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Convert NaN to None for MySQL
    df = df.where(pd.notnull(df), None)

    # Convert date/time fields
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    ).dt.date

    data = list(df.itertuples(index=False, name=None))

    batch_size = 5000

    print("Starting MySQL import...")

    for start in range(0, len(data), batch_size):
        batch = data[start:start + batch_size]

        cursor.executemany(insert_sql, batch)
        connection.commit()

        imported = min(start + batch_size, len(data))

        print(
            f"Imported {imported:,} / {len(data):,} "
            f"({imported / len(data) * 100:.1f}%)"
        )

    cursor.execute("SELECT COUNT(*) FROM raw_transactions")
    count = cursor.fetchone()[0]

    print("\nImport completed!")
    print(f"MySQL rows: {count:,}")

except Error as e:
    print(f"MySQL Error: {e}")

except Exception as e:
    print(f"Error: {e}")

finally:
    try:
        cursor.close()
        connection.close()
    except:
        pass