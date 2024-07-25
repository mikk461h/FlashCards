import pyodbc

class AzureConnect:
    def __init__(self):
        self.conn_string = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=tcp:flashcardss.database.windows.net,1433;"
            "Database=flashcards;"
            "Uid=jappanini;"
            "Pwd={Mette-48};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        self.conn = self.connect()

    def connect(self):
        conn = pyodbc.connect(self.conn_string)
        if conn is not None:
            print("Connection successful!")
        return conn

    def get_connection(self):
        return self.conn

