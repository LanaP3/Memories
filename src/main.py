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
        bottle.redirect("/main_page/") 
        
    
@bottle.get("/main_page/")
def main_page():   
    username = "**USERNAME**"
    albums = [Album(2000/1/1,"**USERNAME**", "album_name",[],[])]     ##user's albums
    images = ["image1"]
    album_name = "**ALBUM_NAME**"
    image_id = "**IMAGE**"
    for album in albums:
        if "album_name" in request.forms:
            bottle.redirect("/album/<album_name>/")
    return bottle.template("main_page.tpl", albums = albums, album_name = album_name, images = images, image_id = image_id, username=username)


@bottle.get("/album/<album_name>/")
def album(album_name):
    username = "**USERNAME**"
    #images = album_name.images()
    images = ["image1"]
    if request.files.get('upload'):
        upload = request.files.get('upload')
        #save_picture(user, upload)
        bottle.redirect('/main_page/')
    return bottle.template("album.tpl", username = username, images = images)

bottle.run(reloader=True, debug=True)
