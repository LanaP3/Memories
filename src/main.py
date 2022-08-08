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
    album = bottle.request.get_cookie("album", secret=CODE)
    if album:
        return Album(album)

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
        if find_user(data, username, password):
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
    username = current_account()
    bottle.response.delete_cookie("album", path="/album/")
    return bottle.template("main_page.tpl", username=username)

#@bottle.post("/main_page/") 
#def main_page_action():
#    username = current_account()
#    album_name = bottle.request.forms.getunicode("new_album")
#    upload = bottle.request.files.get('upload')
#    if current_album():
#        bottle.response.set_cookie("album", current_album(), path="/album/", secret=CODE)
#        bottle.redirect("/album/")
#    elif album_name:
#        username.new_album(album_name)
#    elif upload:
#        username.new_image(upload)
#    
#    bottle.redirect("/main_page/")

@bottle.post("/new_album/")
def create_new_album():
    username = current_account()
    album_name = bottle.request.forms.getunicode("new_album")
    if album_name:
        username.new_album(album_name)
    bottle.redirect("/main_page/")
    
@bottle.post("/add_to_album/")
def add_to_album(image):
    username = current_account()
    album_name = bottle.request.forms.getunicode("album_name")
    if album_name in username.albums:
        album_name.add_image(image) #kera slika??
    return main_page() #izpis "**IMAGE** has been added to **ALBUM**"

@bottle.get("/album/<album_name>")
def albums(album_name):
    username = current_account()
    current_album = Album(album_name,username)
    bottle.response.set_cookie("album", album_name, path="/album/", secret=CODE)
    return bottle.template("album.tpl", friend=None, username=username, album=current_album)

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

@bottle.get("/image/")
def image():
    username = current_account()
    album = current_album()
    image = current_image()


@bottle.post("/log_out/")
def log_out():
    bottle.response.delete_cookie("account", path="/")
    bottle.response.delete_cookie("album", path="/album/")
    bottle.redirect("/")





bottle.run(reloader=True, debug=True)
