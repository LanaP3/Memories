import bottle
import os
import sys
from bottle import get, post, request
from datetime import datetime
from model import *

bottle.TEMPLATE_PATH.insert(0, os.path.join(os.getcwd(), "views"))

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
    if username == "" or password == "":
        return bottle.template("login.tpl", error="Please enter your username and password")       
    else:
        bottle.redirect("/main_page/") 
        
@bottle.get("/main_page/")
def main_page():
    username = "**USERNAME**"
    albums = ["album1", "album2", "album3"] 
    images = ["image1", "image2"]
    return bottle.template("main_page.tpl", albums = albums, images = images, username = username)  
       
@bottle.get("/album/")
def album(friend=None):
    username = "**USERNAME**"
    album ="album1"
    images = ["image1"]
    return bottle.template("album.tpl", likes=1,dislikes=2,friend=friend, album = album, username = username, images = images)


@bottle.post("/log_out/")
def log_out():
    bottle.redirect("/")

@bottle.post("/add_friend/")
def add_friend():
    friend = bottle.request.forms.getunicode("friend")
    if friend == "":
        bottle.redirect("/album/")       
    else:
        return album(friend)
    
@bottle.post("/add_to_album/")
def add_to_album():
    album = bottle.request.forms.getunicode("album")
    if album == "":
        bottle.redirect("/main_page/") 
    else:
        return main_page() #izpis "**IMAGE** has been added to **ALBUM**"

@bottle.post("/album/")
def album_action():
    #for image in album_images:
    #functions: add likes, dislikes, comments
    bottle.redirect("/album/")


bottle.run(reloader=True, debug=True)
