import sqlite3

conn = sqlite3.connect('Test.db')

conn.execute('''CREATE TABLE DATA (
                ID INT PRIMARY KEY NOT NULL,
                NAME TEXT NOT NULL,
                AGE INT NOT NULL,
                ADDRESS CHAR(50) NOT NULL,
                SALARY REAL



                )''')


conn.commit()

conn.close()