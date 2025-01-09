import sqlite3 as sqlite

conn = sqlite.connect('Test.db')

with conn:
    conn.row_factory = sqlite.Row
    curs = conn.cursor()
    rows = curs.execute("SELECT * FROM DATA").fetchall()

    for row in rows:
        print(f"{row['ID']}, {row['NAME']}, {row['AGE']}, {row['ADDRESS']}, {row['SALARY']}.")
        print(type(row['SALARY']))