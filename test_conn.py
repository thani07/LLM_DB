import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=KIS-RLT-KIT047;"
        "DATABASE=chatbot;"
        "UID=sa;"
        "PWD=NewStrongP@ssw0rd!;"
    )
    print("Connected!")
except Exception as e:
    print("ERROR:", e)
