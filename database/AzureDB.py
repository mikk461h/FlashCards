import pyodbc as odbc
import pandas as pd  

conn_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:flashcardss.database.windows.net,1433;"
    "Database=flashcards;"
    "Uid=jappanini;"
    "Pwd={Mette-48};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

try:
    conn = odbc.connect(conn_string)
    print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")
    conn = None

if conn:
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE previously_visited (
        native NVARCHAR(255) NOT NULL,
        translation NVARCHAR(255) NOT NULL,
        progress INT DEFAULT 0,
        status NVARCHAR(50) DEFAULT 'untouched',
        sentence NVARCHAR(255) NOT NULL
    )
    """

    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("Table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()
else:
    print("No connection established. Exiting.")
