from flask import Flask,render_template, request, redirect, url_for, session
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lwk74677;protocol=tcpip;PWD=CnqHgzoxQOU3eVTy",'','')
app = Flask(__name__)

print(conn)

print("DATABASE CONNECTED SUCESSFULLY")