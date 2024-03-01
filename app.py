from asyncio.windows_events import NULL
from flask import Flask, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from flask import render_template

from flask_session import Session

from datetime import datetime

import numpy as np

from flask_mail import Message,Mail

from werkzeug.security import generate_password_hash, check_password_hash
# import pandas as pd

import statistics

# import seaborn as sns

import pickle


import json
# from flask_bootstrap import Boostrap

app = Flask(__name__)

model = pickle.load(open('pickle.pkl','rb')) 

#database configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'detectivesdb'
 
mysql = MySQL(app)

#session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



#Email settings configuartions
   
# configuration of mail
app.config['DEBUG'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
# app.config['MAIL_DEBUG']
app.config['MAIL_USERNAME'] = 'rightwingfelix@gmail.com'
app.config['MAIL_PASSWORD'] = 'coyhdmpjozezjbdd'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# mail = Mail()
# mail.init_app(app)

#End of mail connfigurations
   

#route to display the dashboard
@app.route('/', methods=['GET','POST'])
def renderindex():
    if ('workno' in session) or ('username' in session):      

        cursor = mysql.connection.cursor()
        id = session.get("workno")
        #getting records to update the interface
        sql = """SELECT 2020_declaration_stmt.Workno,2020_declaration_stmt.fname,
                 2020_declaration_stmt.lastname,2022_declaration_stmt.Netdiff,
                 2022_declaration_stmt.statusd FROM
                 2020_declaration_stmt INNER JOIN 2022_declaration_stmt ON
                 2020_declaration_stmt.Workno = 2022_declaration_stmt.Workno;"""
        details = cursor.execute(sql)


        
        #check if there is results returned back
        if details >0:
            returnedata = cursor.fetchall()

            #get the number of count that likely, normal, most likely
            cursor.execute('''SELECT COUNT(statusd) FROM 2022_declaration_stmt WHERE statusd = 'Likely';''')

            likelyc = cursor.fetchall()
            for li in likelyc:
                likely = li[0]
            
            #Count for most likely        
            cursor.execute('''SELECT COUNT(statusd) FROM 2022_declaration_stmt WHERE statusd = 'MostLikely';''')

            mostlikelyc = cursor.fetchall()
            for mli in mostlikelyc:
                mostlikely = mli[0]
            
            #Count for normal        
            cursor.execute('''SELECT COUNT(statusd) FROM 2022_declaration_stmt WHERE statusd = 'Normal';''')

            normalc = cursor.fetchall()
            for norm in normalc:
                normal = norm[0]

            
            #Retrieving records for most likely corrupt individuals
            sql = """SELECT 2020_declaration_stmt.Workno,2020_declaration_stmt.fname,
                 2020_declaration_stmt.lastname,2022_declaration_stmt.Netdiff,
                 2022_declaration_stmt.statusd FROM
                 2020_declaration_stmt INNER JOIN 2022_declaration_stmt ON
                 2020_declaration_stmt.Workno = 2022_declaration_stmt.Workno WHERE
                 statusd='MostLikely';"""
            records2 = cursor.execute(sql)
            mostlikelyrecords = cursor.fetchall()

            #handling chart interface
            #normal data
            normalquery = "SELECT Id FROM 2022_declaration_stmt WHERE statusd = 'Normal';"
            norma = cursor.execute(normalquery)
            
            if norma > 0:
                nor = cursor.fetchall()
            

            #Likely data
            likelyquery = "SELECT Id FROM 2022_declaration_stmt WHERE statusd = 'Likely'"
            like = cursor.execute(likelyquery)
            if like > 0:
                lik = cursor.fetchall()

            #Likely data
            mostlikelyquery = "SELECT Id FROM 2022_declaration_stmt WHERE statusd = 'MostLikely'"
            mostlike = cursor.execute(mostlikelyquery)
            if mostlike > 0:
                mostlik = cursor.fetchall()

            #updates
            query = """SELECT * FROM newsupdates;"""
            cursor.execute(query)
            news = cursor.fetchall()
            #rendering template and passing parameters
            return render_template('indexadmin.html',likely=likely,mostlikely=mostlikely,normal=normal,returnedata=returnedata,mostlikelyrecords=mostlikelyrecords,news=news,nor=json.dumps(nor),lik=json.dumps(lik),mostlik=json.dumps(mostlik))        
        else:
            return f'no data received'
    
    else:
        return redirect('/login')
    

#admin 
@app.route('/admin/dashboard')
def adminpage():
    if 'username' in session:

        cursor = mysql.connection.cursor()
        id = session.get("workno")
        #getting records to update the interface
        sql = """SELECT 2020_declaration_stmt.Workno,2020_declaration_stmt.fname,
                 2020_declaration_stmt.lastname,2022_declaration_stmt.Netdiff,
                 2022_declaration_stmt.statusd,2022_declaration_stmt.probability FROM
                 2020_declaration_stmt INNER JOIN 2022_declaration_stmt ON
                 2020_declaration_stmt.Workno = 2022_declaration_stmt.Workno;"""
        details = cursor.execute(sql)


        
        #check if there is results returned back
        if details >0:
            returnedata = cursor.fetchall()

            #get the number of count that likely, normal, most likely
            cursor.execute('''SELECT COUNT(statusd) FROM 2022_declaration_stmt WHERE statusd = 'Likely';''')

            likelyc = cursor.fetchall()
            for li in likelyc:
                likely = li[0]
            
            #Count for most likely        
            cursor.execute('''SELECT COUNT(statusd) FROM 2022_declaration_stmt WHERE statusd = 'MostLikely';''')

            mostlikelyc = cursor.fetchall()
            for mli in mostlikelyc:
                mostlikely = mli[0]
            
            #Count for normal        
            cursor.execute('''SELECT COUNT(statusd) FROM 2022_declaration_stmt WHERE statusd = 'Normal';''')

            normalc = cursor.fetchall()
            for norm in normalc:
                normal = norm[0]

            
            #Retrieving records for most likely corrupt individuals
            sql = """SELECT 2020_declaration_stmt.Workno,2020_declaration_stmt.fname,
                 2020_declaration_stmt.lastname,2022_declaration_stmt.Netdiff,
                 2022_declaration_stmt.statusd,2022_declaration_stmt.probability FROM
                 2020_declaration_stmt INNER JOIN 2022_declaration_stmt ON
                 2020_declaration_stmt.Workno = 2022_declaration_stmt.Workno WHERE
                 statusd='MostLikely';"""
            records2 = cursor.execute(sql)
            mostlikelyrecords = cursor.fetchall()

            #handling chart interface
            #normal data
            normalquery = "SELECT Id FROM 2022_declaration_stmt WHERE statusd = 'Normal';"
            norma = cursor.execute(normalquery)
            
            if norma > 0:
                nor = cursor.fetchall()
            

            #Likely data
            likelyquery = "SELECT Id FROM 2022_declaration_stmt WHERE statusd = 'Likely'"
            like = cursor.execute(likelyquery)
            if like > 0:
                lik = cursor.fetchall()

            #Likely data
            mostlikelyquery = "SELECT Id FROM 2022_declaration_stmt WHERE statusd = 'MostLikely'"
            mostlike = cursor.execute(mostlikelyquery)
            if mostlike > 0:
                mostlik = cursor.fetchall()

            #updates
            query = """SELECT * FROM newsupdates;"""
            cursor.execute(query)
            news = cursor.fetchall()
            #rendering template and passing parameters
            return render_template('admindashboard.html',likely=likely,mostlikely=mostlikely,normal=normal,returnedata=returnedata,mostlikelyrecords=mostlikelyrecords,news=news,nor=json.dumps(nor),lik=json.dumps(lik),mostlik=json.dumps(mostlik))        
        else:
            return f'no data received'
    
    else:
        return redirect('/admin/login')


#dashboard route
@app.route('/detectiveapp')
def index():
    if ('workno' in session) or ('username' in session):

        return redirect('/')
    
    else:
        return redirect('/login')


#userlogin page
@app.route("/admin/login", methods=['GET','POST'])
def userlogin():
    return render_template('pages-login.html')

#admin handler module
@app.route('/admin/loginhandler',methods=['GET','POST'])
def adminhandle():
    if request.method == 'POST':
        #get the data from the form
        cursor = mysql.connection.cursor()
        admindetails = request.form
        username = admindetails['username']
        password = admindetails['password']
        
        query = '''SELECT password FROM admin_details WHERE email = %s'''
        data = cursor.execute(query,(username,))
        if data > 0:
            fetch = cursor.fetchall()
            for validpass in fetch:
                valid = validpass[0]
            unhashedpass = check_password_hash(valid,password)

            #check if condition to see if the validation is true of false
            if unhashedpass is True:
                session["username"] = username
                return redirect('/admin/dashboard')
            else:
                flash("Invalid credentials, try to register!!!")
                return redirect('/admin/login')
        else:
            flash("Unknown email, try to register!!!")
            return redirect('/admin/login')


#form renderer
@app.route('/signup',methods=['GET','POST'])
def signuprenderer():
    return render_template('pages-register.html')

#signup handler form route
@app.route('/signuphandler',methods=['GET','POST'])
def signupScript():
    if request.method == 'POST':
        userrecord = request.form

        email = userrecord['email']
        username = userrecord['username']
        password = userrecord['password']
        repeatpassword = userrecord['repeatpassword']
        hashedpass = generate_password_hash(password)

        #validating the fields
        if (repeatpassword != password):
            flash("password does not match")
            return redirect('/signup')
        elif len(password) < 5:
            flash("password should have more than 5 characters")
            return redirect('/signup')
        else:

            #connection to the database
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO admin_details VALUES(%s,%s,%s,%s)''',('',username,email,hashedpass))
            mysql.connection.commit()
            cursor.close()
            return redirect('/admin/login')
        
        # return name + '' + email + '' + username + '' + password
        
    
    else:
        return render_template('pages-register.html')

#route for displaying login page
@app.route('/login',methods=['GET','POST'])
def loginuser():
    return render_template('pages-userlogin.html')

#login page handler user
@app.route('/loginhandler', methods=['GET','POST'])
def handleloginuser():
    if request.method == 'POST':
        #get the data from the form
        Logindetails = request.form
        username = Logindetails['username']
        password = Logindetails['password']
       

          #connection to the database
        cursor = mysql.connection.cursor()
        output = cursor.execute("SELECT * FROM 2020_declaration_stmt WHERE Workno = %s and Passwordid=%s",(username,password,))
        

       
        #check if condition 
        if output > 0:
            declaredinfo = cursor.fetchall()
            # return username
            session["workno"] = username
             #getting default password
            passworddefault = cursor.execute("SELECT * FROM 2020_declaration_stmt WHERE Workno = %s and Passwordid = %s",(username,1090))
            # return (session["workno"])
            if passworddefault > 0:
                error = "default"
                return redirect(url_for('renderindex',error=error))
            else:
                return redirect('/detectiveapp')
        else:
            flash("Wrong combination i.e Password and username is incorrect")
            return redirect("/login")



#Updating default password to prevent threats
@app.route('/update/default/password', methods=['GET','POST'])
def updatingpass():
    #check the method used
    if request.method == 'POST':
        data = request.form
        username = session.get('workno')
        #get data 
        currentpassword = data['password'] 
        newpassword = data['newpassword']
        confirmpassword = data['renewpassword']  

        if newpassword != confirmpassword:
            flash('password did not match!')
            return redirect('/user#profile-change-password')
        elif currentpassword == newpassword:
            flash('You can not use the same password!')
            return redirect('/user#profile-change-password')
        else:
            cursor = mysql.connection.cursor()
            output = cursor.execute("SELECT passwordid FROM 2020_declaration_stmt WHERE Workno = %s",(username,))
            
            #check if password exist
            if output > 0:
                fetch = cursor.fetchall()
                for validpass in fetch:
                    valid = validpass[0]
                
                if valid == currentpassword:
                    sql3 = '''UPDATE 2020_declaration_stmt SET Passwordid = %s WHERE Workno = %s'''
                    cursor.execute(sql3,(newpassword,username,))
                    mysql.connection.commit()
                    flash('Succefully updated your password')
                    return redirect('/user#profile-change-password')
                else:
                    flash('wrong current password')
                    return redirect('/user#profile-change-password')


            return redirect('/user#profile-change-password')


#frequent asked questions
@app.route('/faq')
def faq():
    if ('workno' in session) or ('username' in session):

        cursor = mysql.connection.cursor()

        #select questions
        query = '''SELECT subtopic,Topic FROM faq LIMIT 5'''
        quiz = cursor.execute(query)

        if quiz > 0:
            quizdata = cursor.fetchall()
            query2 = '''SELECT subtopic,Topic FROM faq'''
            quiz2 = cursor.execute(query2)
            quizdata2 = cursor.fetchall()
            #pass the data to the frontend design to be used in jinja
            return render_template('pages-faq.html',quizdata=quizdata,quizdata2 = quizdata2)
        else:
            return render_template('pages-faq.html')
    else:
        return redirect('/login')
#userprofile
@app.route('/user')
def returnuser():
    if ('workno' in session) or ('username' in session): 
       id = session.get("workno")
       cursor = mysql.connection.cursor()
       query = """SELECT 2020_declaration_stmt.fname,2020_declaration_stmt.Lastname,employment_info.Employer_name,
                  employment_info.Designation,userinfo.Address,userinfo.time FROM 2020_declaration_stmt INNER JOIN
                  employment_info ON 2020_declaration_stmt.Workno = employment_info.Workno INNER JOIN
                  userinfo ON 2020_declaration_stmt.Workno = userinfo.Workno WHERE userinfo.Workno = %s"""
       data = cursor.execute(query,(id,))
       if data > 0:        
        alldata = cursor.fetchall()        
        return render_template('users-profile.html',alldata=alldata)
       else:
        query2 = """SELECT 2020_declaration_stmt.fname,2020_declaration_stmt.Lastname FROM 
                   2020_declaration_stmt WHERE 2020_declaration_stmt.Workno = %s"""
        partial = cursor.execute(query2,(id,))
        if partial > 0:
            alldt = cursor.fetchall()
            error = "partialerr"
            return render_template('users-profile.html',partial=alldt,error=error)
        else:
            return render_template('users-profile.html')
    else:
        return redirect('/admin/login')
#contact page
@app.route('/contact')
def contactUs():
    if ('workno' in session) or ('username' in session):  
        return render_template('pages-contact.html')             
        # return render_template('pages-contact.html')      
    else:   
        return redirect('/login')

    
#error handler
@app.route('/error')
def renderError():
    return render_template('pages-error-404.html')
    
#signup
# @app.route('/login')
# def LoginScript():
#     return render_template('login.html')


#making declaration
@app.route('/declare')
def wealthdeclare():
    if ('workno' in session) or ('username' in session): 
    #refresh the page by rendering the template
        cursor = mysql.connection.cursor()
        id = session.get("workno")

        #check if the user already exist
        namexist = cursor.execute("""SELECT * FROM userinfo INNER JOIN employment_info
                                    ON userinfo.Workno = employment_info.Workno INNER JOIN
                                    2020_declaration_stmt ON 2020_declaration_stmt.Workno = employment_info.workno
                                    WHERE userinfo.Workno = %s""",(id,))
        if namexist > 0:
            user = cursor.fetchall()

            error = "userexist"
                                     
            
            output = cursor.execute("""SELECT * FROM Assets WHERE Workno = %s""",(id,))

            #check if condition 
            if output > 0:
                declaredinfo = cursor.fetchall()
                
                #Getting income data
                income = cursor.execute("""SELECT * FROM income WHERE Workno = %s""",(id,))
                incomedata = cursor.fetchall()

                #Getting income data
                liable = cursor.execute("""SELECT * FROM liabilities WHERE Workno = %s""",(id,))
                liabledata = cursor.fetchall()
                alreadyexist = cursor.execute("SELECT * FROM 2022_declaration_stmt WHERE Workno = %s",(id,))
        #    return render_template('pages-declaration.html',assetquery=assetquery)
                if alreadyexist > 0:
                    error1 = "already"
                    return render_template('pages-declaration.html', declaredinfo=declaredinfo,incomedata=incomedata,liabledata=liabledata,user=user,error=error,error1=error1)
                else:
                    return render_template('pages-declaration.html', declaredinfo=declaredinfo,incomedata=incomedata,liabledata=liabledata,user=user,error=error)

            else:
                return render_template('pages-declaration.html',user=user,error=error)

            
        else:
            names = cursor.execute('''SELECT * FROM 2020_declaration_stmt WHERE Workno = %s''',(id,))
            if names > 0:
                
                namesdata = cursor.fetchall()
                error = "partial"
                return render_template('pages-declaration.html',namesdata=namesdata, error=error)
            else:
                return render_template('pages-declaration.html')
            # return redirect("/submit/assets")
    
    else:
        return redirect('/login')

#route to handler prediction

@app.route('/predictapi')
def prediction():
    if ('workno' in session) or ('username' in session): 

        #run some sql queries
        id = session.get("workno")
        cursor = mysql.connection.cursor()
        #getting sum of assets
        # sqlquery = '''SELECT sum(assets.Amount) FROM Assets WHERE Workno = %s;'''
        cursor.execute('''SELECT SUM(Amount) FROM Assets WHERE Workno = %s;''',(id,))
        
        dtasset = cursor.fetchall()
        for dts in dtasset:
            asset = dts[0]
        # mysql.connection.commit()

        #getting sum of income
        cursor.execute('''SELECT SUM(Amount) FROM income WHERE Workno = %s;''',(id,))

        dtincome = cursor.fetchall()
        for dti in dtincome:
            income = dti[0]
        # mysql.connection.commit()

        #getting sum of liabilities
        cursor.execute('''SELECT SUM(Amount) FROM liabilities WHERE Workno = %s;''',(id,))

        dtliable = cursor.fetchall()
        for dtl in dtliable:
            liable = dtl[0]
        # mysql.connection.commit()

        #getting salary from previous declaration
        cursor.execute('''SELECT Salaries_income FROM 2020_declaration_stmt WHERE Workno = %s''',(id,))
        salary = cursor.fetchall()
        for salaryin in salary:
            salaryincome = salaryin[0]

        
        #Updating the experience
        cursor.execute('''SELECT Experience FROM 2020_declaration_stmt WHERE Workno = %s''',(id,))
        experience = cursor.fetchall()
        for exp in experience:
            currentexp = exp[0] + 2
        

    
        # mysql.connection.commit()
        # assetquery = 20001
        # return render_template('pages-declaration.html',salary=salary)
        
        # checking if they already submit the declaration
        alreadyexist = cursor.execute("SELECT * FROM 2022_declaration_stmt WHERE Workno = %s",(id,))
        #    return render_template('pages-declaration.html',assetquery=assetquery)
        if alreadyexist > 0:
            flash("You've Already made a declaration")
            error = "already"
            return redirect(url_for('wealthdeclare',error=error))
            # return render_template('pages-declaration.html')
        
        else:
            if (asset is None) or (income is None) or (liable is None):
                flash("Declare at least one asset, income and liablity")
                return redirect('/declare')

            else:
                cursor.execute('''INSERT INTO 2022_declaration_stmt VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',('',id,asset,income,liable,'',currentexp,salaryincome,'Normal',0,0.000000))
                mysql.connection.commit()
                return redirect('/auth/model')
        #    if assetupdate:            
        #       return render_template('pages-declaration.html',assetupdate=assetupdate)
        #    else:
        #       return render_template('pages-declaration.html',assetupdate=assetupdate)
    else:
        return redirect('/login')
#route does not exist
@app.route('/*')
def routedoesnotexist():
    return '<h2>404 NOT FOUND</h2>'


@app.route("/submit/declarationId",methods=['GET','POST'])
def formhandler():
    if ('workno' in session) or ('username' in session): 
        if request.method == 'POST':
            declareinfo = request.form

            #getting records from the url

            fname = declareinfo['fname']
            lname = declareinfo['lname']
            dob = declareinfo['tdate']
            place = declareinfo['place']
            marital = declareinfo['marital']
            address = declareinfo['address']
            time = datetime.now()

            #session
            id = session.get("workno")

            #employment information
            designation = declareinfo['designation']
            emname = declareinfo['emname']
            terms = declareinfo['terms']
            wstation = declareinfo['wstation']
            scounty = declareinfo['scounty']

            # return scounty + ''+ terms
            cursor = mysql.connection.cursor()

            #check if the user already exist
            namexist = cursor.execute("""SELECT * FROM userinfo WHERE Workno = %s""",(id,))
            if namexist > 0:
                return redirect('/declare')                
            else:
                #call the cursor
                
                cursor.execute(''' INSERT INTO userinfo VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',('',id,fname,lname,dob,place,marital,address,time))
                mysql.connection.commit()

                cursor.execute('''INSERT INTO employment_info VALUES(%s,%s,%s,%s,%s,%s,%s)''',('',id,designation,emname,terms,wstation,scounty))
                mysql.connection.commit()
                cursor.close()
                return redirect('/declare')

        
        else:
            return f"failed!"

    else:
        return redirect('/login')
#form assets handler
@app.route("/submit/assets",methods=['GET','POST'])
def assetshandler():
    if ('workno' in session) or ('username' in session): 
        #check if post request
        if request.method == 'POST':
            assetsinfo = request.form
            sessionwork = session.get("workno")
            assetsdesc = assetsinfo['assetsdesc']
            amount  = assetsinfo['amount']
            category = assetsinfo['Assetcat']
            date = datetime.now()

            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO assets VALUES(%s,%s,%s,%s,%s,%s)''',('',sessionwork,assetsdesc,category,amount,date))
            mysql.connection.commit()
            cursor.close()

            return redirect('/declare')
    else:
        return redirect('/login')
#form income handler
@app.route("/submit/income",methods=['GET','POST'])
def incomehandler():
    if ('workno' in session) or ('username' in session): 
        #check if post request
        if request.method == 'POST':
            assetsinfo = request.form

            assetsdesc = assetsinfo['incomedesc']
            amount  = assetsinfo['amount']
            category = assetsinfo['incomecat']
            sessionwork = session.get("workno")
            date = datetime.now()

            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO income VALUES(%s,%s,%s,%s,%s,%s)''',('',sessionwork,assetsdesc,category,amount,date))
            mysql.connection.commit()
            cursor.close()

            return redirect('/declare')
    else:
        return redirect('/login')

#form liabilities handler
@app.route("/submit/liabilities",methods=['GET','POST'])
def liabilitieshandler():
    if ('workno' in session) or ('username' in session): 
        #check if post request
        if request.method == 'POST':
            assetsinfo = request.form

            assetsdesc = assetsinfo['liabilitiesdesc']
            amount  = assetsinfo['amount']
            category = assetsinfo['liabilitiescat']
            sessionwork = session.get("workno")
            date = datetime.now()


            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO liabilities VALUES(%s,%s,%s,%s,%s,%s)''',('',sessionwork,assetsdesc,category,amount,date))
            mysql.connection.commit()
            cursor.close()
            # error = 'success'
            return redirect('/declare')
    else:
        return redirect('/login')
#route to get the categories and declare assets, income and liabilities
@app.route('/generateapi/getrecords')
def getrecords():
    cursor = mysql.connection.cursor()
    output = cursor.execute("SELECT * FROM Assets")

    #check if condition 
    if output > 0:
        declaredinfo = cursor.fetchall()

        return render_template('pages-declaration.html', declaredinfo=declaredinfo)
    else:
        return False




#model training
@app.route('/auth/model')
def predictingmodel():

    cursor = mysql.connection.cursor()

    id = session.get("workno")

    data = cursor.execute('''SELECT Assets,income,liabilities,Experience,
                             salary FROM 2022_declaration_stmt WHERE Workno=%s''',(id,))

    #check if condition
    if data > 0:
        rowdata = cursor.fetchall()
        # finaldata = [np.array(rowdata)]

        #reading a pickle file  
        predict = model.predict(rowdata) 
        output = round(predict[0],1)       
        # return render_template('pages-declaration.html',predict=output)
        #we update the networth
        sql = '''UPDATE 2022_declaration_stmt SET Networth = %s WHERE Workno = %s'''
        updatedt = cursor.execute(sql,(output,id,))
        mysql.connection.commit()

        #check if condition to see update occureed
        if updatedt > 0:
            return redirect('/arithmetic/disclosure/detector')
        
        else:
            return f'failed to update'
            # return redirect('/login')

        
        #Arithmetic logic to test misinterpretation of facts
        #check  accumulated wealth
        #check accumulated assets
        #check business income
        #check salary income 
        #update the status

       
    else:
        return False





#route for checking arithmetic logic
@app.route('/arithmetic/disclosure/detector')
def detection():
    #Arithmetic logic to test misinterpretation of facts
    id = session.get("workno")
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT Networth FROM 2020_declaration_stmt WHERE Workno = %s;''',(id,))

    netwoth2020 = cursor.fetchall()
    for net in netwoth2020:
        networth = net[0]

    #Getting netwoth of the previous declaration

    cursor.execute('''SELECT Networth FROM 2022_declaration_stmt WHERE Workno = %s;''',(id,))

    netwoth2022 = cursor.fetchall()
    for net2 in netwoth2022:
        networth2 = net2[0]

    #calculating probabilities
    percent = (networth/networth2)

    # update the differences in netwoth
    diff = networth2-networth
    sql3 = '''UPDATE 2022_declaration_stmt SET Netdiff = %s WHERE Workno = %s'''
    cursor.execute(sql3,(diff,id,))
    mysql.connection.commit()

    sql4 = '''UPDATE 2022_declaration_stmt SET probability = %s WHERE Workno = %s'''
    cursor.execute(sql4,(percent,id,))
    mysql.connection.commit()
    
    #check sensitivity of declaration
    #measurements
    m1 = "Normal"
    m2 = "Likely"
    m3 = "MostLikely"
    m4 = "Unable"

    if  (networth2 > (networth*4)) and (networth2 < (networth*10)):

        #check another condition using nested if statements
        
        sql = '''UPDATE 2022_declaration_stmt SET statusd = %s WHERE Workno = %s'''
        cursor.execute(sql,(m2,id,))
        mysql.connection.commit()

        return redirect('/')

    elif (networth2 > (networth*10)):
        sql = '''UPDATE 2022_declaration_stmt SET statusd = %s WHERE Workno = %s'''
        cursor.execute(sql,(m3,id,))
        mysql.connection.commit()
        return redirect('/')

    elif (networth2 <= (networth*4)) and (networth2 >= networth):
        sql = '''UPDATE 2022_declaration_stmt SET statusd = %s WHERE Workno = %s'''
        cursor.execute(sql,(m1,id,))
        mysql.connection.commit()
        # return f'done'
        return redirect('/')
    else:
        sql = '''UPDATE 2022_declaration_stmt SET statusd = %s WHERE Workno = %s'''
        cursor.execute(sql,(m2,id,))
        mysql.connection.commit()
        return redirect('/')



#route to handle logout
@app.route('/logout')
def logoutUser():
    session.pop("workno", None)
    return redirect('/login')

#logout admin
@app.route('/admin/logout')
def logoutAdmin():
    session.pop("username", None)
    return redirect('/admin/login')


@app.route('/test')
def test():
    return render_template('a.html')




#Email sending handler

@app.route('/auth/email/formhandler', methods=['GET','POST'])
def handlerEmail():

    #check if condition to see post request
    if request.method == 'POST':
        messagefromform = request.form

        #Extract that message
        message = messagefromform['message']
        subject = messagefromform['subject']
        name = messagefromform['name']
        email = messagefromform['email']

        msg = Message(subject, sender = email,recipients = ['rightwingfelix@gmail.com'])
        msg.html = '''
                    <table class="body-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; background-color: #f6f6f6; margin: 0;" bgcolor="#f6f6f6">
                        <tbody>
                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                                <td class="container" width="600" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;"
                                    valign="top">
                                    <div class="content" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;">
                                        <table class="main" width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; border-radius: 3px; background-color: #fff; margin: 0; border: 1px solid #e9e9e9;"
                                            bgcolor="#fff">
                                            <tbody>
                                                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                    <td class="" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 16px; vertical-align: top; color: #fff; font-weight: 500; text-align: center; border-radius: 3px 3px 0 0; background-color: #38414a; margin: 0; padding: 20px;"
                                                        align="center" bgcolor="#71b6f9" valign="top">
                                                        <a href="#" style="font-size:32px;color:#fff;"> Wealthdeclaration.com</a> <br>
                                                        <span style="margin-top: 10px;display: block;">Updates: You've a new message from a client".</span>
                                                    </td>
                                                </tr>
                                                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                    <td class="content-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 20px;" valign="top">
                                                        <table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                            <tbody>
                                                                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                    <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                        You have <strong style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">1
                                                    unread email</strong> please read it.
                                                                    </td>
                                                                </tr>
                                                                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                    <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                        message
                                                                    </td>
                                                                </tr>
                                                                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                    <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                        <a href="#" class="btn-primary" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #f1556c; margin: 0; border-color: #f1556c; border-style: solid; border-width: 8px 16px;">Click here to reply
                                                                        </a>
                                                                    </td>
                                                                </tr>
                                                                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                    <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                        Thanks for choosing <b>wealth declaration platform</b> Admin.
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <div class="footer" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; clear: both; color: #999; margin: 0; padding: 20px;">
                                            <table width="100%" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                <tbody>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="aligncenter content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 12px; vertical-align: top; color: #999; text-align: center; margin: 0; padding: 0 0 20px;" align="center" valign="top"><a href="#" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 12px; color: #999; text-decoration: underline; margin: 0;">Unsubscribe</a> from these alerts.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </td>
                                <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                            </tr>
                        </tbody>
                    </table>'''
        msg.body = 'Hello  receive warm greetings'
        mail.send(msg)

        return True


#detecting outliers
@app.route('/detecting/outliers')
def detectingoutliers():

    #execute a query
    id = session.get("workno")
    cursor = mysql.connection.cursor()

    query = '''SELECT Networth FROM 2020_declaration_stmt'''
    data = cursor.execute(query)

    

    #if condition
    if data > 0:
        datall = cursor.fetchall()
        finaldata = np.array(datall)
        mean = np.mean(finaldata)
        stdev = np.std(finaldata)
        #Getting netwoth of the previous declaration
        cursor.execute('''SELECT Networth FROM 2022_declaration_stmt WHERE Workno = %s;''',(id,))

        netwoth2022 = cursor.fetchall()
        for net2 in netwoth2022:
            networth2 = net2[0]
        # mean = statistics.mean(datall)
        # stdev = statistics.stdev(datall)
        #if sigma rule

        #most likely to be corrupt
        #anomaly in the dataset
        if ((networth2-mean) > 3*stdev):
            return f'Most likely'
        
        #likely to accumulate wealth of larger quantity
        elif ((networth2-mean) > 2.5*stdev) or ((networth2-mean) < 3*stdev):
            return render_template('pages-declaration.html',stdev=stdev,mean=mean)

        elif ((networth2-mean) > 2*stdev) or ((networth2-mean) < 2.5*stdev):
            return f'Normal'

        elif ((networth2-mean) > stdev) or ((networth2-mean) < 2*stdev):
            return f'likely'

        elif ((networth2-mean) < stdev):
            return 'under estimated'

        else:
            return f'unable to predict'

    else:
        return f'no records found'

#sending alerts to an Secretary officer to do further investigation
@app.route('/sending/alertsdetector/')
def sendingAlerts():
    msg = Message(
                'Hello',
                sender ='rightwingfelix@gmail.com',
                recipients = ['felixlopuran@gmail.com']
               )
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg)

    return f'sent'


#manipulating declared data
@app.route('/deleteAsset/<id>')
def getDeletedAsset(id):
    
    #delete item from the database
    cursor = mysql.connection.cursor()
    # return 'welcome %s' %id
    query = '''DELETE FROM assets WHERE Id = %s'''
    deleted = cursor.execute(query,(id,))
    mysql.connection.commit()

    if deleted > 0:
        return redirect('/declare')
    else:
        return f'failed to deleted the item'

    return 'id gotten %s' %id

@app.route('/deleteLiability/<id>')
def getDeletedLiability(id):
    
    #delete item from the database
    cursor = mysql.connection.cursor()
    # return 'welcome %s' %id
    query = '''DELETE FROM liabilities WHERE Id = %s'''
    deleted = cursor.execute(query,(id,))
    mysql.connection.commit()

    if deleted > 0:
        return redirect('/declare')
    else:
        return f'failed to deleted the item'

    return 'id gotten %s' %id

@app.route('/deleteincome/<id>')
def getDeletedIncome(id):
    
    #delete item from the database
    cursor = mysql.connection.cursor()
    # return 'welcome %s' %id
    query = '''DELETE FROM income WHERE Id = %s'''
    deleted = cursor.execute(query,(id,))
    mysql.connection.commit()

    if deleted > 0:
        return redirect('/declare')
    else:
        return f'failed to deleted the item'

    return 'id gotten %s' %id


#handler non-existing routes
@app.errorhandler(404)
def page_notfound(e):
    return render_template("pages-error-404.html"),404




if __name__ == '__main__':
    app.run(debug=True)
    



#classes for handling

# class handlingRegister():
#     formdata = StringField()
