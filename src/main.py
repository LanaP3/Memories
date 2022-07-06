import bottle
import os
import sys
from bottle import get, post, request
from datetime import datetime
from model import *

bottle.TEMPLATE_PATH.insert(0, os.path.join(os.getcwd(), "view"))

@bottle.get("/")
def login_page():
    return bottle.template("login.tpl", error=None)

@bottle.post("/")
def login_post():
    username = bottle.request.forms.getunicode("username")
    password = bottle.request.forms.getunicode("password")
    if username == "" or password == "":
        return bottle.template("login.tpl", error="Please enter your username and password")       
    else:
        #bottle.response.set_cookie("username", username, path="/")
        bottle.redirect("/home_page/") 
        
    
@bottle.get("/home_page/")
def home_page():
    return bottle.template("home_page.tpl", username="...USERNAME...")

#@bottle.post("/home_page/")
#def home_post():
#    if bottle.request.


bottle.run(reloader=True)
