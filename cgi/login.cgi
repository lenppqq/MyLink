#!/usr/bin/python
# -*- coding: utf-8 -*-
# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random, Cookie
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
from session import *
from ptn import *
from datetime import datetime

#Get Databasedir
MYLOGIN="liangp"
DATABASE="/homes/"+MYLOGIN+"/MyLink/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/MyLink/images"

##############################################################
# Define function to generate login HTML form.
def login_form():
    print_html_content_type()
    print_til_nav("Login")
    html="""
                <ul class="nav navbar-nav navbar-right">
                    <li class="active"><a href="/login.cgi">Login</a></li>
                    <li><a href="/create.cgi">Create an Account</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <h1>Login</h1></br>
    <FORM METHOD=post ACTION="/" style="width:400;">
        <div class="form-group">
            <label for="username">Username</label>
            <INPUT class="form-control" TYPE=text NAME="username" id="username">
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <INPUT class="form-control" TYPE=password NAME="password" id="password">
        </div>
        <div class="form-group">
            <INPUT TYPE=hidden NAME="action" VALUE="login">
            <button type="submit" class="btn btn-default">Submit</button>
        </div>
    </FORM>
</BODY>
</HTML>
"""
    print(html)



###################################################################
# Define function to test the password.
def check_password(user, passwd):

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)

    row = stored_password=c.fetchone()
    conn.close();

    if row != None: 
      stored_password=row[1]
      if (stored_password==passwd):
         return "passed"

    return "failed"

##########################################################
# Diplay the options of admin
def display_admin_options(c):
    print_html_content_type()
    username=c["user"].value
    print_til_nav_logged("Timeline",c)
    conn = sqlite3.connect(DATABASE)
    cu = conn.cursor()
    t = (username,)
    cu.execute('SELECT id, name from circles where email=?', t)
    circles=cu.fetchall()
    
    print("""
        <FORM ACTION="/" METHOD="POST" enctype="multipart/form-data" style="width:600px">
            <div class="form-group">
                <textarea class="form-control" rows="3" name="msg"></textarea>
            </div>
            <div class="form-group">
                <INPUT TYPE="FILE" NAME="file">
            </div>
            <div class="form-group">
                <button class="btn btn-default" type="button" data-toggle="collapse" data-target="#circles" aria-expanded="false" aria-controls="circles">
                    Edit Visibility
                </button>
                <button class="btn btn-success" type="submit">
                    Submit
                </button>
            </div>
            <INPUT TYPE="hidden" NAME="action" value="post">
            <div class="form-group panel panel-default collapse" id="circles">
                <div class="btn-group" data-toggle="buttons">
            """)
    for cir in circles:
        if cir[0]==1:
            print("""
                    <label class="btn btn-info active">
                        <input type="checkbox" name="circles" value="1" autocomplete="off" checked>All Friends
                    </label>""")
        else:
            print("""
                    <label class="btn btn-info">
                        <input type="checkbox" name="circles" value="{}" autocomplete="off">{}
                    </label>""".format(cir[0], cir[1]))
    print("""
                </div>
            </div>
        </form>
        <div style="width:600px">""")
    cu.execute('select emaila, circles from relations where emailb=?', (username,))
    friends_circles=cu.fetchall()
    result = []
    for fc in friends_circles:
        crlist=fc[1].split('.')
        crcond=' ('
        for cr in range(1, len(crlist)-1):
            crcond=crcond+" circles like '%.{}.%' ".format(crlist[cr])
            if cr == len(crlist)-2:
                crcond = crcond + ')'
            else:
                crcond = crcond + 'or'
        q = "select * from posts where email='{}' and ".format(fc[0]) + crcond
        cu.execute(q)
        result = result + cu.fetchall()
    cu.execute('select * from posts where email =?', (username,))
    result = result + cu.fetchall()
    result.sort(key = lambda x:x[3], reverse = True)
    for r in result:
        cu.execute('select * from pi where email=?',(r[0],))
        pi=cu.fetchone()
        print("""
        <div class="panel panel-info">
            <div class="panel-heading"><img src="{}" class="img-thumbnail" style="height:36px;margin-right:10px;padding:2px;margin-top:-4px;margin-bottom:-4px;">{}</div>
            <div class="panel-body">
                <p>{}</p>
                """.format('login.cgi?action=show_image&path='+pi[2],pi[1], r[1]))
        if r[2]!='null':
            print("""
                <p><img src="{}" class="img-thumbnail"></p>
                """.format('login.cgi?action=show_image&path='+r[2]))
        print("""
                <p class="text-info text-right">{}</p>
            </div>
        </div>
        """.format(r[3].split('.')[0]))
    print("""
    </body>
</html>
        """)
    conn.close()
        #Also set a session number in a hidden field so the
        #cgi can check that the user has been authenticated

#################################################################
def create_new_session(user):
    return session.create_session(user)

##############################################################
def new_album(form, c):
    #Check session
    print_html_content_type()
    html="""
        <H1> New Album</H1>
        """
    print(html);

##############################################################
def show_image(form, c):
    #Check session

    # Your code should get the user album and picture and verify that the image belongs to this
    # user and this album before loading it

    #username=form["username"].value

    # Read image
    path = form['path'].value
    with open(IMAGEPATH+path, 'rb') as content_file:
       content = content_file.read()

    # Send header and image content
    hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
    print hdr+content

###############################################################################

def upload(form, c):
    print_html_content_type()
    print_til_nav_logged("Change User Picture",c)
    html="""


        <FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
            <input type="hidden" name="action" value="upload-pic-data">
            <BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
            <br>
            <button class="btn btn-success" type="submit">Submit</button>
            </form>
            </body>
        </HTML>
    """

    user=c["user"].value
    s=c["session"].value
    print(html.format(user=user,session=s))

#######################################################

def upload_pic_data(form, c):
    #Get file info
    fileInfo = form['file']
    #Get user
    user=c["user"].value
    s=c["session"].value
    print_html_content_type()
    print_til_nav_logged("Change User Picture",c)
    # Check if the file was uploaded
    if fileInfo.filename:
        # Remove directory path to extract name only
        fileName = os.path.basename(fileInfo.filename)
        open(IMAGEPATH+'/up_'+user.replace('@','at'), 'wb').write(fileInfo.file.read())
        conn = sqlite3.connect(DATABASE)
        cu = conn.cursor()
        cu.execute('update pi set picture=? where email=?',('/up_'+user.replace('@','at'), user))
        conn.commit()
        conn.close()
        print('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
    else:
        print 'No file was uploaded'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")

#######################################################
#post a new post
def new_post(form, c):
    circles = "."
    for nc in form.getlist('circles'):
        circles=circles+nc+'.'
    username=c['user'].value
    conn = sqlite3.connect(DATABASE)
    cu = conn.cursor()
    fileInfo = form['file']
    if fileInfo.filename:
        fileName = os.path.basename(fileInfo.filename)
        open(IMAGEPATH+'/'+username.replace('@','at')+'-'+fileName, 'wb').write(fileInfo.file.read())
        image_url='/'+username.replace('@','at')+'-'+fileName
    else:
        image_url='null'
    t = (username, form['msg'].value, image_url, datetime.now(), circles)
    
    conn = sqlite3.connect(DATABASE)
    cu = conn.cursor()
    cu.execute('INSERT INTO posts values (?,?,?,?,?)', t)
    conn.commit()
    conn.close()

    display_admin_options(c)
#######################################################
#post a new post
def change_password(form, c):
    print_html_content_type()
    print_til_nav_logged("Change Password",c)
    html = """
    <FORM METHOD=post ACTION="/" style="width:400;">
        <div class="form-group">
            <label for="passwordo">Old Password</label>
            <INPUT class="form-control" TYPE=password NAME="passwordo" id="passwordo" palceholder="Please enter your email.">
        </div>
        <div class="form-group">
            <label for="password">New Password</label>
            <INPUT class="form-control" TYPE=password NAME="password" id="password">
        </div>
        <div class="form-group">
            <label for="passwordr">Repeat Password</label>
            <INPUT class="form-control" TYPE=password NAME="passwordr" id="passwordr">
        </div>
        <div class="form-group">
            <INPUT TYPE=hidden NAME="action" VALUE="cpassword">
            <button type="submit" class="btn btn-default">Submit</button>
        </div>
    </FORM>"""
    if form['action'].value == 'cpassword' and 'passwordo' in form and 'password' in form and 'passwordr' in form:
        conn = sqlite3.connect(DATABASE)
        cu = conn.cursor()
        cu.execute('select password from users where email=?',(c["user"].value,))
        opass = cu.fetchone()[0]
        if form['passwordo'].value == opass and form['password'].value == form['passwordr'].value:
            cu.execute('update users set password = ? where email = ?',(form['password'].value,c["user"].value,))
            print "Your password has been changed."
            conn.commit()
        else:
            print """<div class="alert alert-danger" role="alert" style="width:400px">The information you entered has some mistakes...</div>"""
            print(html)
        conn.close()
    elif form['action'].value == 'cpassword':
        print """<div class="alert alert-danger" role="alert" style="width:400px">Please fill all the fields</div>"""
        print(html)
    else:
        print(html)
#######################################################
#Manage friends

def pinfo (info):
    print("""<div class="alert alert-info" role="alert" style="width:400px">{}</div>""".format(info))
def perror (info):
    print("""<div class="alert alert-danger" role="alert" style="width:400px">{}</div>""".format(info))


def mf(form, c):
    conn = sqlite3.connect(DATABASE)
    cu = conn.cursor()
    if form['action'].value == "rf":#Remove Friend
        print_html_content_type()
        print_til_nav_logged("Manage Friends",c)
        cu.execute('delete from relations where emaila = ? and emailb = ?',
            (form['femail'].value, c['user'].value))
        cu.execute('delete from relations where emailb = ? and emaila = ?',
            (form['femail'].value, c['user'].value))
        conn.commit()
        print("""<div class="alert alert-info" role="alert" style="width:400px">Friend deleted</div>""")
    elif form['action'].value == "sr":#Send Request
        print_html_content_type()
        print_til_nav_logged("Manage Friends",c)
        if 'femail' in form:
            if form['femail'].value==c['user'].value:
                pinfo("Haha, interesting.")
            else:
                cu.execute('select * from users where email =?', (form['femail'].value,))
                if cu.fetchone()!=None :
                    cu.execute('select * from relations where emailb=? and emaila=?',
                        (form['femail'].value,c['user'].value))
                    r = cu.fetchone()
                    cu.execute('select * from relations where emaila=? and emailb=?',
                        (form['femail'].value,c['user'].value))
                    rr = cu.fetchone()
                    if r==None and rr==None:
                        cu.execute('insert into relations values (?,?,?)',(c['user'].value, form['femail'].value, '.0.'))
                        conn.commit()
                        pinfo("Request Sent!")
                    elif (r[2].startswith(".1.")):
                        pinfo("You two are already friends.")
                    elif (r[2].startswith(".0.")):
                        pinfo("You've already sent a request.")
                    elif (rr[2].startswith(".0.")):
                        pinfo("That person has already sent a request to you.")
                else:
                    pinfo("We can't find this person...")
        else:
            pinfo("You didn't enter anything.")
    elif form['action'].value == 'af':#Add Friend
        cu.execute('delete from relations where emaila = ? and emailb = ?',
            (form['femail'].value, c['user'].value))
        cu.execute('delete from relations where emailb = ? and emaila = ?',
            (form['femail'].value, c['user'].value))
        cu.execute('insert into relations values (?,?,?)',
            (form['femail'].value, c['user'].value, '.1.'))
        cu.execute('insert into relations values (?,?,?)',
            (c['user'].value, form['femail'].value, '.1.'))
        conn.commit()
        print_html_content_type()
        print_til_nav_logged("Manage Friends",c)
        print("""<div class="alert alert-success" role="alert" style="width:400px">Friend Added!</div>""")
    elif form['action'].value == 'df':#Deny Friend
        cu.execute('delete from relations where emaila = ? and emailb = ?',
            (form['femail'].value, c['user'].value))
        cu.execute('delete from relations where emailb = ? and emaila = ?',
            (form['femail'].value, c['user'].value))
        conn.commit()
        print_html_content_type()
        print_til_nav_logged("Manage Friends",c)
    elif form['action'].value == 'uc':#Update Circle
        circles='.1.'
        for nc in form.getlist('circles'):
            circles=circles+nc+'.'
        cu.execute('update relations set circles=? where emaila=? and emailb=?',
            (circles, c['user'].value, form['femail'].value))
        conn.commit()
        print_html_content_type()
        print_til_nav_logged("Manage Friends",c)
        print("""<div class="alert alert-success" role="alert" style="width:400px">Circles Updated!</div>""")

    #Request form
    else:
        print_html_content_type()
        print_til_nav_logged("Manage Friends",c)
    print("""
    <FORM METHOD=post ACTION="/" style="width:600px;"> 
        <div class="form-group">
            <label for="email">Add a Friend</label>
            <div class="input-group">
                <input name="femail" type="text" class="form-control" id="email" placeholder="Friend's Email">
                <span class="input-group-btn"><button type="submit" class="btn btn-primary">Send Request</button></span>
            </div>
        </div>
        <input type="hidden" name="action" value="sr">
    </form>
    """)
    #Request Received
    cu.execute("select emaila from relations where emailb=? and circles = '.0.'", (c['user'].value,))
    rqs=cu.fetchall()
    if len(rqs)>0:
        print("""<p><label>Friend Requests</label></p>""")
        print("""
    <table class="table table-hover" style="width:600px;">""")
        for rq in rqs:
            cu.execute('select name from pi where email=?',(rq[0],))
            name = cu.fetchone()[0]
            print("""
        <tr>
                <td>{} ({})</td>
                <td align=right>
                <form METHOD=post ACTION="/"> 
                <button class="btn btn-success" type="submit" name="action" value="af">Accept</button>
                <button class="btn btn-danger" type="submit" name="action" value="df">Ignore</button>
                <input type="hidden" name="femail" value="{}">
            </form>
        </tr>
                """.format(name,rq[0],rq[0]))
        print("""
    </table>
        """)
    #Friends' list
    cu.execute("SELECT emailb, circles from relations where circles like '.1%' and emaila=? ", (c['user'].value,))
    friends = cu.fetchall()
    print("""
    <table class="table table-hover" style="width:600px;">""")
    frn=0
    cu.execute("select id, name from circles where email =?", (c['user'].value,))
    circles = cu.fetchall()
    for fr in friends:
        cu.execute('select name from pi where email=?',(fr[0],))
        name = cu.fetchone()[0]
        print("""
        <tr>
                <td>{} ({})</td>
                <td align=right>
                    <button type="button" class="btn btn-info" data-toggle="modal" data-target="#cform{}">Circles</button>
                    <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#fform{}">Remove</button>
                </td>
                <div id="fform{}" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
                  <div class="modal-dialog modal-sm">
                    <div class="modal-content">
                        <div class="modal-header">
                            You want to remove {} from your friend list?
                        </div>
                        <div class="modal-footer">
                            <form METHOD=post ACTION="/"> 
                                <button type="button" class="btn btn-default" data-dismiss="modal">No</button>
                                <button class="btn btn-danger" type="submit">Remove Friend</button>
                                <input type="hidden" name="action" value="rf">
                                <input type="hidden" name="femail" value="{}">
                            </form>
                        </div>
                    </div>
                  </div>
                </div>
                """.format(name,fr[0],frn,frn,frn,name,fr[0]))
        #Circles form
        print("""
                <div id="cform{}" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            Circles for {}
                        </div>
                        <div class="modal-body">
                        <form METHOD=post ACTION="/"> 
                            <div class="btn-group" data-toggle="buttons">""".format(frn, name))
        for cir in circles:
            if cir[0]!=1:
                if fr[1].find('.'+str(cir[0])+'.')==-1:
                    print("""
                                <label class="btn btn-info">
                                    <input type="checkbox" name="circles" value="{}" autocomplete="off">{}
                                </label>""".format(cir[0], cir[1]))
                else:
                    print("""
                                <label class="btn btn-info active">
                                    <input type="checkbox" name="circles" value="{}" autocomplete="off" checked>{}
                                </label>""".format(cir[0], cir[1]))
        print("""
                            </div>
                        </div>
                        <div class="modal-footer">
                            
                                <button type="button" class="btn btn-default" data-dismiss="modal">No</button>
                                <button class="btn btn-success" type="submit">Confirm</button>
                                <input type="hidden" name="action" value="uc">
                                <input type="hidden" name="femail" value="{}">
                            </form>
                        </div>
                    </div>
                  </div>
                </div>
            """.format(fr[0]))
        print ("</tr>")
        frn=frn+1
    print("""
    </table>
        """)
    conn.close()

#######################################################
#Manage Circles

def mc(form, c):
    conn = sqlite3.connect(DATABASE)
    cu = conn.cursor()
    print_html_content_type()
    print_til_nav_logged("Manage Circles",c)
    if form['action'].value=='cc':#Create circle
        if 'cn' in form:
            cu.execute('select * from circles where email=? and name=?',
                (c['user'].value, form['cn'].value))
            scircle = cu.fetchone()
            if scircle==None:
                #There isn't such a circle, g2g
                cu.execute('select max(id) as mcid from circles where email=?',
                    (c['user'].value,))
                mcidt = cu.fetchone()[0]
                if mcidt == None:
                    mcid = 2
                else:
                    mcid = mcidt + 1
                cu.execute('insert into circles values (?,?,?)',
                    (c['user'].value, mcid,form['cn'].value))
                conn.commit()
                pinfo("Circle Added!")
            else:
                perror("There's already a circle named {}".format(form['cn'].value))
        else:
            perror("You didn't enter anything...")
    elif form['action'].value=='rc':
        q='delete from circles where email="{}" and id={}'.format(c['user'].value, form['cid'].value)
        cu.execute(q)
        cu.execute('select * from relations where emaila=? and circles like ?',
            (c['user'].value, '%.'+form['cid'].value+'.%'))
        frs=cu.fetchall()
        for fr in frs:
            cu.execute('update relations set circles = ? where emaila =? and emailb=?',
                (fr[2].replace('.'+form['cid'].value+'.', '.'), 
                    c['user'].value, fr[1]))
        cu.execute('select * from posts where email=? and circles like ?',
            (c['user'].value, '%.'+form['cid'].value+'.%'))
        ps=cu.fetchall()
        for p in ps:
            cu.execute('update posts set circles = ? where email =?',
                (p[2].replace('.'+form['cid'].value+'.', '.'), 
                    c['user'].value))
        conn.commit()
        pinfo("Circle deleted.")

    #Create circle form
    print("""
    <FORM METHOD=post ACTION="/" style="width:500px;"> 
        <div class="form-group">
            <label for="cn">Create a Circle</label>
            <div class="input-group">
                <input name="cn" type="text" class="form-control" id="cn" placeholder="Circle Name">
                <span class="input-group-btn"><button type="submit" class="btn btn-primary">Create</button></span>
            </div>
        </div>
        <input type="hidden" name="action" value="cc">
    </form>
    """)
    #show the circle list
    print("""
    <table class="table table-hover" style="width:500px;">""")
    cu.execute('select * from circles where email = ?', (c['user'].value,))
    crs=cu.fetchall()
    for cr in crs:
        if cr[1]!=1:
            print("""
        <tr>
                <td>{}</td>
                <td align=right>
                <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#cform{}">Delete</button>
                </td>
                <div id="cform{}" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
                  <div class="modal-dialog modal-sm">
                    <div class="modal-content">
                        <div class="modal-header">
                            You want to remove Circle "{}"?
                        </div>
                        <div class="modal-footer">
                            <form METHOD=post ACTION="/"> 
                                <button type="button" class="btn btn-default" data-dismiss="modal">No</button>
                                <button class="btn btn-danger" type="submit">Confirm</button>
                                <input type="hidden" name="action" value="rc">
                                <input type="hidden" name="cid" value={}>
                            </form>
                        </div>
                    </div>
                  </div>
                </div>
        </tr>
                """.format(cr[2],cr[1],cr[1],cr[2],cr[1]))
    print("""
    </table>
            """)
    conn.close()
##############################################################
# Update Personal Info
def upi(form, c):
    conn = sqlite3.connect(DATABASE)
    cu = conn.cursor()
    print_html_content_type()
    print_til_nav_logged("Update Info",c)
    if form['action'].value=='upi':
        cu.execute('update pi set name = ? where email = ?',
            (form['nickname'].value, c['user'].value))
        conn.commit()
        pinfo("Your nickname is updated!")
    cu.execute('select name from pi where email=?', (c['user'].value,))
    r=cu.fetchone()
    print("""
    <FORM METHOD=post ACTION="/" style="width:400;">
        <div class="form-group">
            <label for="nickname">Nickname</label>
            <INPUT class="form-control" TYPE=text NAME="nickname" id="nickname" value="{}">
        </div>
            <INPUT TYPE=hidden NAME="action" VALUE="upi">
            <button type="submit" class="btn btn-default">Submit</button>
    </FORM>""".format(r[0]))
    conn.close()
##############################################################
# Define main function.
def main():
    form = cgi.FieldStorage()
    if "action" in form:
        action=form["action"].value
        if action == "logout":
            c=Cookie.SimpleCookie()
            c['user']=''
            c['user']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'
            c['session']=''
            c['session']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'
            print(c)
            login_form()
        elif action == "login":
            if "username" in form and "password" in form:
                #Test password
                username=form["username"].value
                password=form["password"].value
                if check_password(username, password)=="passed":
                    session=create_new_session(username)
                    c=Cookie.SimpleCookie()
                    c['user']=username
                    c['session'] = session
                    c['user']['expires'] =3600*3
                    c['session']['expires'] =3600*3
                    print(c)
                    display_admin_options(c)
                else:
                    login_form()
                    print("""<div class="alert alert-danger" role="alert" style="width:400px">Wrong username or password</div>""")
            else:
                login_form()
                print("""<div class="alert alert-danger" role="alert" style="width:400px">Please fill all fields!</div>""")
        elif 'HTTP_COOKIE' in os.environ:
            cookie_string=os.environ.get('HTTP_COOKIE')
            c=Cookie.SimpleCookie()
            c.load(cookie_string)
            if check_session_cookies(c) == "passed":
                c['user']['expires'] =3600*3
                c['session']['expires'] =3600*3
                print(c)
                if (action == "timeline"):
                    display_admin_options(c)
                elif (action == "post"):
                    new_post(form, c)
                elif (action == "new-album"):
                    new_album(form, c)
                elif (action == "upload"):
                    upload(form, c)
                elif (action == "show_image"):
                    show_image(form, c)
                elif action == "upload-pic-data":
                    upload_pic_data(form, c)
                elif action == "password" or action == "cpassword":
                    change_password(form, c)
                elif action == 'update' or action=='upi':
                    upi(form, c)
                elif action=='df' or action=='uc' or action == "mf" or action == "rf" or action=="sr" or action=="af":
                    mf(form, c)
                elif action=='mc' or action=="cc" or action=="rc":
                    mc(form, c)
                else:
                    display_admin_options(c)
            else:
                login_form()
        else:
            login_form()
    elif 'HTTP_COOKIE' in os.environ:
        cookie_string=os.environ.get('HTTP_COOKIE')
        c=Cookie.SimpleCookie()
        c.load(cookie_string)
        if check_session_cookies(c) == "passed":
            c['user']['expires'] =3600*3
            c['session']['expires'] =3600*3
            print(c)
            display_admin_options(c)

        else:
            login_form()
    else:
        login_form()
    #YEAH CHECK FOR FRequest


###############################################################
# Call main function.
main()
