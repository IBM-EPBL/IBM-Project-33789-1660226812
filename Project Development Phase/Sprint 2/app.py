from flask import Flask,render_template,request, redirect, url_for, session
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lwk74677;PWD=CnqHgzoxQOU3eVTy",'','')
app = Flask(__name__)


@app.route("/")
def log():
  # return render_template('LoginRegister.html', name="login")
  return render_template('home.html', name="home")

@app.route('/register',methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':

    name = request.form['name']
    mail=request.form['mail']
    pwd=request.form['pwd']
    cpwd=request.form['cpwd']
    cno=request.form['cno']
    
    sql = "SELECT * FROM signup WHERE mail =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,mail)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      return render_template('LoginRegister.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO signup VALUES (?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, mail)
      ibm_db.bind_param(prep_stmt, 3, pwd)
      ibm_db.bind_param(prep_stmt, 4, cpwd)
      ibm_db.bind_param(prep_stmt, 5, cno)
      ibm_db.execute(prep_stmt)
    
    return render_template('home.html', msg="Data saved successfully..")

@app.route('/login',methods=['POST'])
def login():
  mail=request.form['mail']
  pwd=request.form['pwd']
  sql = "SELECT * FROM signup WHERE mail =? AND password=?"
  stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(stmt,1,mail)
  ibm_db.bind_param(stmt,2,pwd)
  ibm_db.execute(stmt)
  account = ibm_db.fetch_assoc(stmt)
  if account:
    #return redirect(url_for('home'))
    return render_template('dashboard.html') 
  else:
    return render_template('loginRegister.html', pred="Login unsuccessful. Incorrect username / password !") 

@app.route('/loginn')
def loginn():
  return render_template('LoginRegister.html')

@app.route('/registerr')
def registerr():
   return render_template('LoginRegister.html')


if __name__ == "__main__":
    app.run(debug=True)