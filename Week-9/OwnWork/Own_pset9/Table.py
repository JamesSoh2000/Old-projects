import sqlite3

# ./ means it is the current directory
con = sqlite3.connect("./finance.db")

# ???? Table 이 없는데 already exist 라함
con.execute('''CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price NUMERIC NOT NULL,
        type TEXT NOT NULL,
        symbol TEXT NOT NULL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

con.commit()
con.close()