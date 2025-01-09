from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

con = sql.connect("database.db")
cur = con.cursor()

@app.route('/')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      # My Version !!!
      try:

         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']

         cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
         con.commit()
         msg = "Record successfully added"

      except:
         # con.rollback()이 위에서 con.commit()으로 저장한것을 다시 바로전 상태로 되돌림.
         con.rollback()
         msg = f"{nm} error in insert operation"

      finally:
         return render_template("result.html",msg = msg)
         con.close()

      # try:
      #    nm = request.form['nm']
      #    addr = request.form['add']
      #    city = request.form['city']
      #    pin = request.form['pin']

      #    with sql.connect("database.db") as con:
      #       cur = con.cursor()

      #       cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )

      #       con.commit()
      #       msg = "Record successfully added"
      # except:
      #    # con.rollback()이 위에서 con.commit()으로 저장한것을 다시 바로전 상태로 되돌림.
      #    con.rollback()
      #    msg = f"{nm} error in insert operation"

      # finally:
         # return render_template("result.html",msg = msg)
         # con.close()


@app.route('/list')
def list():
   # con = sql.connect("database.db")
   con.row_factory = sql.Row

   # cur = con.cursor()
   cur.execute("select * from students")

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)
   con.close()

if __name__ == '__main__':
   app.run()