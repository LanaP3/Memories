import bottle
import os
import sys
from bottle import get, post, request
from datetime import datetime

from click import password_option
from model import *

bottle.TEMPLATE_PATH.insert(0, os.path.join(os.getcwd(), "view"))

@bottle.get("/")
def login_page():
    return bottle.template("login.tpl", error=None)

@bottle.post("/")
def login_post():
    username = bottle.request.forms.getunicode("Username")
    password = bottle.request.forms.getunicode("Password")
    if username and password:
        bottle.redirect("/home_page/")
    else:
        return bottle.template("login.tpl", error="Wrong password")

@bottle.get("/home_page/")
def home_page():
    return bottle.template("home_page.tpl")

bottle.run(reloader=True)
