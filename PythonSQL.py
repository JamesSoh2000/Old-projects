import sqlite3

con = sqlite3.connect('Test.db')

cursor = con.cursor()
# print(cursor.execute("PRAGMA table_info('DATA')").fetchall())

# cursor.execute("INSERT INTO DATA values (1, 'James', 17, 'Avinue-120', 360000)")
cursor.execute("INSERT INTO DATA values (2, 'Jamie', 17, 'Avinue-18', 260000)")

# [(1, 'James', 17, 'Avinue-17', 360000.0), (2, 'Jamie', 17, 'Avinue-18', 260000.0)]



# 여기 이 두개의 용도는 위에 있는 것들로 인한 병경점들을 모두 저장하는 것임.
con.commit()

con.close()