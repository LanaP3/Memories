from attr import define
import bottle
import os
import sys
from bottle import get, post, request
from datetime import datetime
from model import *

path_to_code = os.path.join(os.getcwd(),'..', "database", "secret.txt")
with open(path_to_code, "r") as d:
    CODE = d.read()

app = bottle.default_app()
bottle.BaseTemplate.defaults['get_url'] = app.get_url

def current_account():
    username = bottle.request.get_cookie("account", secret=CODE)
    if username is None:
        bottle.redirect("/log_in/")
    else:
        return User(username)        

def current_album():
    album_name = bottle.request.get_cookie("album", secret=CODE)
    account = current_account()
    if album_name:
        return Album(album_name, account)

def current_image():
    image = bottle.request.get_cookie("image", secret=CODE)
    if image:
        pass
    else:
        bottle.redirect("/album/")

@bottle.get('/database/<filename:path>', name='database')
def serve_static(filename):
    return bottle.static_file(filename, root= os.path.join(os.getcwd(),'..', "database"))

@bottle.get("/log_in/")
def log_in():
    return bottle.template("login.tpl", error=None)

#a fix loci med username,password za log in in za register?
@bottle.post("/log_in/")
def do_login():
    username = bottle.request.forms.getunicode("username")
    password = bottle.request.forms.getunicode("password")
    if username and password:
        data = read_json()
        if find_account(data, username, password):
            bottle.response.set_cookie("account", username, path="/", secret=CODE)
            bottle.redirect("/")
        else:
            return bottle.template("login.tpl", error="Your password is incorrect.")
    else:
        return bottle.template("login.tpl", error="Please enter your username and password.")        

@bottle.post("/register/")
def register():
    username = bottle.request.forms.getunicode("username")
    password = bottle.request.forms.getunicode("password")
    if username and password:
        data = read_json()
        if username_available(data, username):
            User.register(username, password)
            bottle.response.set_cookie("account", username, path="/", secret=CODE)
            bottle.redirect("/")
        else:
            return bottle.template("login.tpl", error="Please choose another username.")             
    else:
        return bottle.template("login.tpl", error="Please enter your username and password.") 

@bottle.get("/")
def memories():
    bottle.redirect("/main_page/")

@bottle.get("/main_page/")
def main_page():
    account = current_account()
    bottle.response.delete_cookie("album", path="/")
    return bottle.template("main_page.tpl", account=account)

@bottle.post("/new_album/")
def create_new_album():
    account = current_account()
    album_name = bottle.request.forms.getunicode("new_album")
    if album_name:
        account.new_album(album_name)
    bottle.redirect("/main_page/")
    
@bottle.post("/add_to_album/")
def add_to_album(image):
    account = current_account()
    album_name = bottle.request.forms.getunicode("album_name")
    if album_name in account.albums:
        album_name.add_image(image) #kera slika??
    bottle.redirect("/main_page/") #izpis "**IMAGE** has been added to **ALBUM**"

@bottle.post("/album/<album_name>")
def enter_album(album_name):
    bottle.response.set_cookie("album", album_name, path="/", secret=CODE)
    bottle.redirect("/album/")

@bottle.get("/album/")
def albums(error=None):
    account = current_account()
    album = current_album()
    return bottle.template("album.tpl", error=error, account=account, album=album)

@bottle.post("/add_friend/")
def add_friend():
    account = current_account()
    album = current_album()
    friend_name = bottle.request.forms.getunicode("friend")
    data = read_json()
    error = None
    if account.username == album.owner.username:
        if friend_name in data:
            if friend_name not in album.access:
                error = f"Your friend {friend_name} has been added to album."
                album.change_access(account, friend_name)
    if error == None:
        error = "Please enter your friends username."  
    return albums(error)                              


@bottle.get("/image/")
def image():
    account = current_account()
    album = current_album()
    image = current_image()


@bottle.post("/log_out/")
def log_out():
    bottle.response.delete_cookie("account", path="/")
    bottle.response.delete_cookie("album", path="/")
    bottle.redirect("/")





bottle.run(reloader=True, debug=True)
