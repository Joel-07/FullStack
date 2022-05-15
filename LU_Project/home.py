import requests
from flask import Flask, jsonify, request, render_template, redirect,session,make_response
from flask.helpers import flash
from flask.wrappers import Response
import mysql.connector as mc
import time,datetime
from werkzeug.datastructures import ResponseCacheControl

app = Flask(__name__)
app.secret_key="abc" #for session
db=mc.connect(host="localhost",user="root",password="12345678",database="sars")
myc=db.cursor(buffered=True)

# myc.execute("create database sars")
# db.commit()
url="https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=f5e58788&app_key=505b36bdaa98b0a45f6a3c887808c71a&content-type=application/json"
res=requests.get(url).json()["results"]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET","POST"])
def regis():
    if request.method == 'GET':
        return render_template("reg.html")

    else:
        try:
            sid=time.time()
            nm = request.form.get('name')
            em= request.form.get('email')
            mbno = request.form.get('mob')
            passw = request.form.get('password')
            gen = request.form.get('gender')
            dob = request.form.get('dob')
            city = request.form.get('city')
            addr = request.form.get('addr')
            pin = request.form.get('pin')
            st = request.form.get('state')
            myc.execute("select email from stureg")
            eml=myc.fetchall()
            eml=[i[0] for i in eml]
            if em in eml:
                return redirect("/login")
            # myc.execute("create table stureg(stuid int primary key,stuname varchar(100) not null,email varchar(50) not null ,mobileno int(10),password varchar(100) not null,gender varchar(10) not null,dob varchar(50) not null,city varchar(50) not null,address varchar(400) not null,pin varchar(20) not null,state varchar(50) not null)")
            myc.execute("insert into stureg (stuid,stuname,email,mobileno,password,gender,dob,city,address,pin,state) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(sid,nm,em,mbno,passw,gen,dob,city,addr,pin,st))
            db.commit()
        except Exception as e:
            print(e)
        return redirect("/login")

# @app.route("/login", methods=["GET","POST"])#without session or cookies
# def normallogin():
#     if request.method=="GET":
#         return render_template("login.html")
#     else:
#         global un
#         un=request.form.get('user')
#         pas=request.form.get('pass')
#         myc.execute("select * from stureg where email='"+un+"' and password='"+pas+"'")
#         #myc.execute("select * from stureg where email= %s and password= %s",(un,pas))
#         a=myc.fetchone()
#         if a:
#             return render_template("jobs.html",data=a[1])
#         else:
#             return "wrong username or password"


@app.route("/sessionlogin", methods=["GET","POST"]) #using session
def sessionlogin():
    if request.method=="GET":
        return render_template("login.html")
    else:
        global un
        session.pop("un",None)
        session['un']=request.form.get('user')
        session['pas']=request.form.get('pass')
        # myc.execute("select * from stureg where email='"+un+"' and password='"+pas+"'")
        myc.execute("select * from stureg where email= %s and password= %s",(session['un'],session['pas']))
        a=myc.fetchone()
        print(a[2],session)
        if a[2] in session['un']:
            return render_template("jobs.html",data=a[1])
        else:
            return "wrong username or password"

@app.route("/login", methods=["GET","POST"])#using cookies
def login():
        if request.method=="POST":
            if request.form.get('user'):
                un=request.form.get('user')
                pas=request.form.get('pass')
                # myc.execute("select * from stureg where email='"+un+"' and password='"+pas+"'")
                myc.execute("select * from stureg where email= %s and password= %s",(un,pas))
                a=myc.fetchone()
                if a:
                    resp= make_response(render_template('jobs.html',data=a[1],result=res))
                    resp.set_cookie("user",un)
                    return resp
                else:
                    flash('Wrong email or password', 'error')
            else:
                un=request.form.get('uname')
                pas=request.form.get('pas')
                # myc.execute("select * from stureg where email='"+un+"' and password='"+pas+"'")
                myc.execute("select * from cmpreg where email= %s and password= %s",(un,pas))
                a=myc.fetchone()
                if a:
                    resp= make_response(render_template('dashboard.html',data=a[1]))
                    resp.set_cookie("user",un)
                    return resp
                else:
                    flash('Wrong email or password', 'error')        

        un=request.cookies.get('user')
        if un:
            myc.execute("select * from stureg where email= %s",(un,))
            d=myc.fetchone() 
            if d==None:
                myc.execute("select * from cmpreg where email= %s",(un,))
                d=myc.fetchone()
                return render_template("dashboard.html",data=d[1])                  
            return render_template("jobs.html",data=d[1],result=res)
        else:
            return render_template("login.html")

@app.route("/logout", methods=["GET","POST"])#using cookies
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('user') 
    return resp




@app.route("/cregister", methods=["GET","POST"])
def cregis():
    if request.method == 'GET':
        return render_template("reg.html")

    else:
        try:
            cid=time.time()
            cnm = request.form.get('cname')
            rnm = request.form.get('rname')
            mbno = request.form.get('mob')
            em= request.form.get('email')            
            passw = request.form.get('pass')           
            cweb = request.form.get('csite')           
            city = request.form.get('city')
            st = request.form.get('state')
            
            myc.execute("select email from cmpreg")
            eml=myc.fetchall()
            eml=[i[0] for i in eml]
            if em in eml:
                flash('Email Exist', 'error')
                return render_template("reg.html")

            # myc.execute("create table cmpreg(cid int primary key,cname varchar(100) not null,rname varchar(100) not null,mobileno int not null,email varchar(50) not null ,password varchar(100) not null,cwebsite varchar(40),city varchar(50) not null,address varchar(400) not null,pin varchar(20) not null,state varchar(50) not null)")
            # myc.execute("alter table cmpreg drop address,drop pin")
            myc.execute("insert into cmpreg (cid,cname,rname,mobileno,email,password,cwebsite,city,state) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(cid,cnm,rnm,mbno,em,passw,cweb,city,st))
            db.commit()
        except Exception as e:
            print(e)
        return redirect("/clogin")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method=="GET":
        return render_template("contact.html")

@app.route("/about", methods=["GET","POST"])
def about():
    if request.method=="GET":
        return render_template("index.html")

@app.route("/myaccount",methods=["GET","POST"])
def myaccount():
    un=request.cookies.get('user')
    myc.execute("select * from stureg where email= %s",(un,))
    d=myc.fetchone()
    return render_template("myacc.html",data=d)

@app.route("/profile",methods=['GET','POST'])
def profile():
    un=request.cookies.get('user')
    myc.execute("select * from stureg where email= %s",(un,))
    d=myc.fetchone()
    if request.method=='POST':
        em= request.form.get('email')
        mbno = request.form.get('mob')
        dob = request.form.get('dob')
        gen = request.form.get('gender')
        st = request.form.get('state')
        addr = request.form.get('addr')

        myc.execute("update stureg set dob=%s where email=%s",(dob,em))
        db.commit()
        return render_template("profile.html",data=d)
    return render_template("profile.html",data=d)

@app.route("/postjob",methods=['GET','POST'])
def postjob():
    if request.method=='POST':
        jt=request.form.get('title')
        jd=request.form.get('desc')
        jl=request.form.get('loc')
        typ=request.form.get('type')
        cn=request.form.get('cname')
        cat=request.form.get('cat')
        ur=request.form.get('url')
        cd=request.form.get('cdesc')
        cw=request.form.get('cweb')
        print(jt,jd,jl,typ,cat,ur,cn,cd,cw)
        return render_template("dashboard.html")
    print(datetime.datetime.strftime("%Y","%m","%d"))
    un=request.cookies.get('user')
    myc.execute("select * from cmpreg where email= %s",(un,))
    d=myc.fetchone()
    return render_template("postjob.html",data=d[1])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
