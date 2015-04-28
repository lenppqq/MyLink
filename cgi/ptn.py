#!/usr/bin/python
import sqlite3
DATABASE="/homes/"+"liangp"+"/MyLink/picture_share.db"
def print_til_nav(title):
    print("""
<HTML>
<HEAD>
    <meta name="viewport" content="width=device-width -70px, initial-scale=1" />
    <meta charset="utf-8">
    <TITLE>"""+title+""" | MyLink</TITLE>
    
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
<BODY BGCOLOR = white style="padding-top:70px;padding-left:70px;">
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
            <div class="collapse navbar-collapse" id="lr" >""")
def print_til_nav_logged(title,c):
    conn = sqlite3.connect(DATABASE)
    cu = conn.cursor()
    cu.execute('select * from relations where emailb=? and circles=".0."', (c['user'].value,))
    r=cu.fetchall()
    if len(r)>0:
        bd='<span class="badge" style="margin-left:3px">{}</span>'.format(len(r))
    else:
        bd=''
    print("""
<HTML>
<HEAD>
    <meta name="viewport" content="width=device-width - 70px, initial-scale=1" />
    <meta charset="utf-8">
    <TITLE>"""+title+""" | MyLink</TITLE>
    
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
<BODY BGCOLOR = white style="padding-top:70px;padding-left:70px;">
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
            <div class="collapse navbar-collapse" id="lr" >""")
    print("""
                <ul class="nav navbar-nav">
                    <li><a href="/?action=mf">Manage Friends{}</a></li>
                    <li><a href="/?action=mc">Manage Circles</a></li>
                    <li><a href="/?action=update">Update Info</a></li>
                    <li><a href="/?action=upload">Upload Picture</a></li>
                </ul>
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="/?action=password">Change Password</a></li>
                    <li><a href="/?action=logout">Logout</a></li>
                </ul>
            </div>
        </div>
    </nav>""".format(bd))
def print_left():
    print("""
            </div>
        </div>
    </nav>""")