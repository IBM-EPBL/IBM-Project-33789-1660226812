from flask import Flask, render_template, request, redirect, session 
import re
import datetime
import sendgrid
from flask_db2 import DB2
import ibm_db
import ibm_db_dbi
import os
from sendemail import sendmail
app = Flask(__name__)

app.secret_key = 'a'

app.config['database'] = 'bludb'
app.config['hostname'] = '9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud'
app.config['port'] = '32459'
app.config['protocol'] = 'tcpip'
app.config['uid'] = 'lwk74677'
app.config['pwd'] = 'CnqHgzoxQOU3eVTy'
app.config['security'] = 'SSL'
app.config['SSLServerCertificate']='DigiCertGlobalRootCA.crt'
try:
    mysql = DB2(app)

    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lwk74677;protocol=tcpip;PWD=CnqHgzoxQOU3eVTy",'','')
        
    print("Database connected without any error !!")
except:
    print("IBM DB Connection error   :     " + DB2.conn_errormsg()) 

#HOME--PAGE
@app.route("/home")
def home():
    return render_template("dashboard.html")
@app.route("/")
def add():
    return render_template("home.html")

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    
    if request.method == 'POST' :
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
            return render_template('login.html', msg="You are already a member, please login using your details")
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


@app.route("/signin",methods=['post','get'])
def signin():
    if request.method=="post":
        return render_template("login.html")
    return render_template("login.html")

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        mail = request.form['mail']
        pwd = request.form['pwd']
        sql = "SELECT * FROM signup WHERE mail =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,mail)
        ibm_db.bind_param(stmt,2,pwd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        param = "SELECT * FROM signup WHERE mail = " + "\'" + mail + "\'" + " and password = " + "\'" + pwd + "\'"
        res = ibm_db.exec_immediate(conn, param)
        dictionary = ibm_db.fetch_assoc(res)
        if account:
            session['loggedin'] = True
            # session["id"] = dictionary["ID"]
            # userid = dictionary["ID"]
            session['name'] = dictionary["NAME"]
            session['mail'] = dictionary["MAIL"]
           
            return render_template('dashboard.html') 
            # return redirect('/homepage')
        else:
           msg = 'Incorrect username / password !!'
    return render_template('login.html', msg = msg)
@app.route("/add")
def adding():
    return render_template('add.html')

@app.route('/addexpense',methods=['GET', 'POST'])
def addexpense():
    
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']

    print(date)
    p1 = date[0:10]
    p2 = date[11:13]
    p3 = date[14:]
    p4 = p1 + "-" + p2 + "." + p3 + ".00"
    print(p4)
    # date=datetime.datetime.now().date()
    sql = "INSERT INTO expenses (userid, date, expensename, amount, paymode, category) VALUES (?,?, ?, ?, ?, ?)"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['mail'])
    ibm_db.bind_param(stmt, 2, p4)
    ibm_db.bind_param(stmt, 3, expensename)
    ibm_db.bind_param(stmt, 4, amount)
    ibm_db.bind_param(stmt, 5, paymode)
    ibm_db.bind_param(stmt, 6, category)
    ibm_db.execute(stmt)

    print("Expenses added")

 # email part

    param = "SELECT * FROM expenses WHERE MONTH(date) = MONTH(current timestamp) AND YEAR(date) = YEAR(current timestamp) ORDER BY date DESC"
   
    res = ibm_db.exec_immediate(conn, param)
    print("passed")
    dictionary = ibm_db.fetch_assoc(res)
    expense = []
    while dictionary != False:
        temp = []
        # temp.append(dictionary["ID"])
        temp.append(dictionary["USERID"])
        temp.append(dictionary["DATE"])
        temp.append(dictionary["EXPENSENAME"])
        temp.append(dictionary["AMOUNT"])
        temp.append(dictionary["PAYMODE"])
        temp.append(dictionary["CATEGORY"])
        expense.append(temp)
        print(temp)
        dictionary = ibm_db.fetch_assoc(res)

    total=0
    for x in expense:
        total += int(x[3])
        
    print(total)
    
#DISPLAY---graph 

@app.route("/display")
def display():
    # print(session["username"],session['id'])
    # param = "SELECT * FROM expense WHERE userid = " + str(session['mail']) + " ORDER BY date DESC"
    param="SELECT * FROM expenses"
    res = ibm_db.exec_immediate(conn, param)
    dictionary = ibm_db.fetch_assoc(res)
    print(dictionary)
    expense = []
    while dictionary != False:
        temp = []
        # temp.append(dictionary["ID"])
        temp.append(dictionary["USERID"])
        temp.append(dictionary["DATE"])
        temp.append(dictionary["EXPENSENAME"])
        temp.append(dictionary["AMOUNT"])
        temp.append(dictionary["PAYMODE"])
        temp.append(dictionary["CATEGORY"])
        expense.append(temp)
        print(temp)
        dictionary = ibm_db.fetch_assoc(res)

    return render_template('display.html' ,expense = expense)
                          
