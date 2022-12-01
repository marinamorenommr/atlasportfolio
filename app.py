from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/about')
def about():
   return render_template('about.html')   

@app.route('/projects')
def projects():
   return render_template('projects.html')

@app.route('/contact')
def contact():
   return render_template('contact.html')

#this code was adapted from an example, as the example was not working
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         name = request.form['name']
         company = request.form['company']
         email = request.form['email']
         message = request.form['message']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO contacts (name,company,email,message) VALUES (?,?,?,?)",(name,company,email,message) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from contacts")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)



if __name__ == '__main__':
    app.run(debug=True)   