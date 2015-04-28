#!/usr/bin/python
# -*- coding: utf-8 -*-
# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
import re
import smtplib  
from email.mime.text import MIMEText

#Get Databasedir
MYLOGIN="liangp"
DATABASE="/homes/"+MYLOGIN+"/MyLink/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/MyLink/images"

def create_form():
    html="""
<HTML>

<HEAD>
    <meta charset="utf-8">
    <TITLE>Register | MyLink</TITLE>
    
    <script src="./jquery-2.1.3.min.js"></script>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    
    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
    
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

    <style type="text/css">
        *{
        transition: all 0.3s, background-position 1ms;
        -o-transition: all 0.3s, background-position 1ms;
        -moz-transition: all 0.3s, background-position 1ms;
        -webkit-transition: all 0.3s, background-position 1ms;
        }
        .btn:hover{
        background-position: 0px 0px !important;
        }
    </style>
</HEAD>
<BODY BGCOLOR = white style="padding-top:70px;padding-left:70px;padding-right:70px;">
    <nav class="navbar navbar-default navbar-fixed-top navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#lr">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">MyLink</a>
            </div>
            <div class="collapse navbar-collapse" id="lr" >
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="login.cgi">Login</a></li>
                    <li class="active"><a href="/create.cgi">Create an Account</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <h1>Create a New Account</h1></br>
    <FORM METHOD=post ACTION="create.cgi" style="width:400;">
        <div class="form-group">
            <label for="username">Email:</label>
            <INPUT class="form-control" TYPE=text NAME="username" id="username" placeholder="Please enter your email.">
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <INPUT class="form-control" TYPE=password NAME="password" id="password">
        </div>
        <div class="form-group">
            <label for="passwordr">Repeat Password</label>
            <INPUT class="form-control" TYPE=password NAME="passwordr" id="passwordr">
        </div>
        <div class="form-group">
            <INPUT TYPE=hidden NAME="action" VALUE="create">
            <button type="submit" class="btn btn-default">Submit</button>
        </div>
    </FORM>
</BODY>
</HTML>
"""
    print(html)

#if the username exist, return 0
def check_user(user):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)
    row = c.fetchone()
    conn.close()
    if row != None: 
      return 0
    return 1

def check_tempuser(user):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = (user,)
    c.execute('SELECT * FROM tempusers WHERE email=?', t)
    row = c.fetchone()
    conn.close()
    if row != None: 
      return 0
    return 1
def resend(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('select * from tempusers where email=?', (username,))
    row = c.fetchone()
    conn.close()
    code = row[2]
    body="""Go to this link to verify your account:
<a href="http://sslab02.cs.purdue.edu:54264/create.cgi?v="""+code+"""">Verify</a>
If you cannot click the link, copy this URL and paste into you browser: 
http://sslab02.cs.purdue.edu:54264/create.cgi?v="""+code
    msg=MIMEText(body,_subtype='html')
    fromaddr="liangp@purdue.edu"
    msg['Subject'] = 'Active your account!'
    msg['From'] = fromaddr
    msg['To'] = username
    s=smtplib.SMTP("localhost")
    s.set_debuglevel(1)
    s.sendmail(fromaddr, [username], msg.as_string())
    s.quit()
    print("""
<HTML>
<HEAD>
    <meta charset="utf-8">
    <TITLE>Register | MyLink</TITLE>
    
    <script src="./jquery-2.1.3.min.js"></script>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    
    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
    
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

    <style type="text/css">
        *{
        transition: all 0.3s, background-position 1ms;
        -o-transition: all 0.3s, background-position 1ms;
        -moz-transition: all 0.3s, background-position 1ms;
        -webkit-transition: all 0.3s, background-position 1ms;
        }
        .btn:hover{
        background-position: 0px 0px !important;
        }
    </style>
</HEAD>
<BODY BGCOLOR = white style="padding-top:70px;padding-left:70px;padding-right:70px;">
    <nav class="navbar navbar-default navbar-fixed-top navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#lr">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">MyLink</a>
            </div>
            <div class="collapse navbar-collapse" id="lr" >
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="login.cgi">Login</a></li>
                    <li class="active"><a href="/create.cgi">Create an Account</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <h1>One More Step...</h1>
    We have sent a verification email to """+username+""" 
    </br>
    Check your email and click the verification link please!
</BODY>
</HTML>
        """)
def create_user(user, passwd):
    char_set = string.ascii_uppercase + string.digits
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    code = ''.join(random.sample(char_set,20))
    qdata=(user, passwd, code,)
    c.execute('INSERT INTO tempusers VALUES (?,?,?)', qdata)
    conn.commit()
    conn.close()
    body="""Go to this link to verify your account:
<a href="http://sslab02.cs.purdue.edu:54264/create.cgi?v="""+code+"""">Verify</a>
If you cannot click the link, copy this URL and paste into you browser: 
http://sslab02.cs.purdue.edu:54264/create.cgi?v="""+code
    msg=MIMEText(body,_subtype='html')
    fromaddr="liangp@purdue.edu"
    msg['Subject'] = 'Active your account!'
    msg['From'] = fromaddr
    msg['To'] = user
    s=smtplib.SMTP("localhost")
    s.set_debuglevel(1)
    s.sendmail(fromaddr, [user], msg.as_string())
    s.quit()
    print("""
<HTML>
<HEAD>
    <meta charset="utf-8">
    <TITLE>Register | MyLink</TITLE>
    
    <script src="./jquery-2.1.3.min.js"></script>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    
    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
    
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

    <style type="text/css">
        *{
        transition: all 0.3s, background-position 1ms;
        -o-transition: all 0.3s, background-position 1ms;
        -moz-transition: all 0.3s, background-position 1ms;
        -webkit-transition: all 0.3s, background-position 1ms;
        }
        .btn:hover{
        background-position: 0px 0px !important;
        }
    </style>
</HEAD>
<BODY BGCOLOR = white style="padding-top:70px;padding-left:70px;padding-right:70px;">
    <nav class="navbar navbar-default navbar-fixed-top navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#lr">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">MyLink</a>
            </div>
            <div class="collapse navbar-collapse" id="lr" >
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="login.cgi">Login</a></li>
                    <li class="active"><a href="/create.cgi">Create an Account</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <h1>One More Step...</h1>
    We have sent a verification email to """+user+""" 
    </br>
    Check your email and click the verification link please!
</BODY>
</HTML>
        """)
def verify_account(vcode):
    print("""
<HTML>
<HEAD>
    <meta charset="utf-8">
    <TITLE>Verify | MyLink</TITLE>
    
    <script src="./jquery-2.1.3.min.js"></script>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    
    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
    
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

    <style type="text/css">
        *{
        transition: all 0.3s, background-position 1ms;
        -o-transition: all 0.3s, background-position 1ms;
        -moz-transition: all 0.3s, background-position 1ms;
        -webkit-transition: all 0.3s, background-position 1ms;
        }
        .btn:hover{
        background-position: 0px 0px !important;
        }
    </style>
</HEAD>
<BODY BGCOLOR = white style="padding-top:70px;padding-left:70px;padding-right:70px;">
    <nav class="navbar navbar-default navbar-fixed-top navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#lr">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">MyLink</a>
            </div>
            <div class="collapse navbar-collapse" id="lr" >
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="login.cgi">Login</a></li>
                    <li class="active"><a href="/create.cgi">Create an Account</a></li>
                </ul>
            </div>
        </div>
    </nav>""")
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = (vcode,)
    c.execute('SELECT * FROM tempusers WHERE code=?', t)
    row = stored_password=c.fetchone()
    if row != None: 
        u=row[0];
        p=row[1];
        c.execute('INSERT INTO users VALUES (?,?)', (u, p))
        c.execute('INSERT INTO circles VALUES (?,?,?)', (u, 1, "Friends"))
        c.execute('INSERT INTO pi values (?,?,?)', (u, u, '/grey-avatar-2.png'))
        c.execute('DELETE FROM tempusers where code=?', (t))
        conn.commit()
        print("""
    <h1>Welcome!</h1>
    You have verify your account!
    </br>
    Now login and share your pictures!
</BODY>
</HTML>""")
    else:
        print("""
    <h1>Something went wrong...</h1>
    <div class="alert alert-danger" role="alert" style="width:400px">
        We cannot verify any account through this link...
    </div>
    </br>
    Probably you didn't copy the link completely.
</BODY>
</HTML>""")
    conn.close()
def main():
    form = cgi.FieldStorage()
    print("Content-Type: text/html\n\n")
    if "v" in form:
        vcode = form["v"].value
        verify_account(vcode)
    elif "action" in form:
        action=form["action"].value
        if action == "rev":
            username=form["username"].value
            resend(username)
        elif action == "create":
            if "username" in form and "password" in form:
                username=form["username"].value
                password=form["password"].value
                passwordr=form["passwordr"].value
                if not re.match(r"""[^@]+@[^@]+\.[^@]+""", username):
                    create_form()
                    print("""<div class="alert alert-danger" role="alert" style="width:400px">Please enter your email as your password!</div>""")
                elif password != passwordr:
                    create_form()
                    print("""<div class="alert alert-danger" role="alert" style="width:400px">Your entered two different passwords!</div>""")
                elif check_user(username) == 0:
                    create_form()
                    print("""<div class="alert alert-danger" role="alert" style="width:400px">Username has been taken!</div>""")
                elif check_tempuser(username) == 0:
                    create_form()
                    print("""
    <div class="alert alert-danger" role="alert" style="width:400px">Username has been taken but not verified!</div>
    <FORM METHOD=post ACTION="create.cgi" style="width:400;">
        <div class="form-group">
            <INPUT TYPE=hidden NAME="action" VALUE="rev">
            <INPUT TYPE=hidden NAME="username" VALUE="""+'"'+username+'"'+""">
            <button type="submit" class="btn btn-primary">Click here to resend your verification email</button>
        </div>
    </FORM>""")
                else:
                    create_user(username, password)
            else:
                create_form()
                print("""<div class="alert alert-danger" role="alert" style="width:400px">Please fill all fields!</div>""")
        else:
            create_form()
    else:
        create_form()
main()
