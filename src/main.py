import bottle
import os
import sys
from bottle import get, post, request
from datetime import datetime
from model import *

bottle.TEMPLATE_PATH.insert(0, os.path.join(os.getcwd(), "views"))
with open('secret.txt') as d:
    CODE = d.read()

def current_account():
    username = bottle.request.get_cookie("account", secret=CODE)
    if username:
        return find_user(username)
    else:
        bottle.redirect("/login/")

def current_album():
    album = bottle.request.get_cookie("album", secret=CODE)
    if album:
        pass
    else:
        bottle.redirect("/main_page/")


@bottle.route('/database/<filename:path>', name='database')
def serve_static(filename):
    return bottle.static_file(filename, root= os.path.join(os.getcwd(),'..', "database"))

@bottle.get("/")
def login():
    return bottle.template("login.tpl", error=None)

@bottle.post("/")
def do_login():
    username = bottle.request.forms.getunicode("username")
    password = bottle.request.forms.getunicode("password")
    if username and password:
        data = read_json()
        if find_user(data, username, password):
            bottle.response.set_cookie("account", username, path="/main_page/", secret=CODE)
            bottle.redirect("/main_page/")          
    else:
        return bottle.template("login.tpl", error="Please enter your username and password.") 
        
@bottle.get("/main_page/")
def main_page():
    username = current_account()
    if current_album():
        bottle.response.delete_cookie("album")
    return bottle.template("main_page.tpl", username=username)  
       
@bottle.get("/album/")
def album(friend=None):
    username = current_account()
    album = current_album()
    return bottle.template("album.tpl", friend=friend, username=username, album=album)


@bottle.post("/log_out/")
def log_out():
    bottle.response.delete_cookie("account")
    if current_album():
        bottle.response.delete_cookie("album")
    bottle.redirect("/")

@bottle.post("/add_friend/")
def add_friend():
    username = current_account()
    album = current_album()
    friend = bottle.request.forms.getunicode("friend")
    if friend == "":
        bottle.redirect("/album/")       
    else:
        album.change_access(username, friend)
        return album()
    
@bottle.post("/add_to_album/")
def add_to_album():
    username = current_account()
    if album == "":
        bottle.redirect("/main_page/") 
    else:
        album = bottle.request.forms.getunicode("album")
        album.add_image("image") #kera slika??
        return main_page() #izpis "**IMAGE** has been added to **ALBUM**"

@bottle.post("/album/")
def enter_album():
    album = bottle.request.forms.getunicode("album")
    bottle.response.set_cookie("album", album, path="/album/", secret=CODE)
    bottle.redirect("/album/")


bottle.run(reloader=True, debug=True)
