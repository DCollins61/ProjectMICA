from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def list():
   print("Connection Established!\n")
   con = sql.connect("member_data.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from Members")
   
   return render_template("list.html",rows = cur.fetchall())

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
