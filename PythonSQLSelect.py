import sqlite3

con = sqlite3.connect('Test.db')

cursor = con.cursor()

# Update the age as 5, where ID is 1.
cursor.execute('UPDATE DATA SET AGE = 5 WHERE ID = 1').fetchall()

decoy = cursor.execute('SELECT * FROM DATA').fetchall()

print(decoy)
print(decoy[0][0])

cursor.close()
con.close()



