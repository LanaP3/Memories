from attr import define
import bottle
import os
import sys
from bottle import get, post, request
from datetime import datetime
from model import *
#te pripise, errorje bi lahko dala da se vsi na istem mestu vedno izpisejo, npr. okvircek desno zgoraj
#dodaj ikonce

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
    album_id = bottle.request.get_cookie("album", secret=CODE)
    if album_id:
        return Album(album_id)
    else:
        bottle.redirect("/main_page/")

def current_image():
    image_id = bottle.request.get_cookie("image", secret=CODE)
    album = current_album()
    album_id = album.id
    if image_id:
        return Picture(image_id, album_id)
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
        if User.find_account(username, password):
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
        if User.username_available(username):
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
    list_of_albums = account.get_albums()
    bottle.response.delete_cookie("album", path="/")
    bottle.response.delete_cookie("image", path="/")
    return bottle.template("main_page.tpl", account=account, list_of_albums=list_of_albums)

@bottle.post("/upload_image/")
def upload_image():
    account = current_account()
    upload = bottle.request.files.get('upload')
    account.new_image(upload)
    bottle.redirect("/main_page/")

@bottle.post("/new_album/")
def create_new_album():
    account = current_account()
    album_id = bottle.request.forms.getunicode("new_album")
    if album_id:
        account.new_album(album_id)
    bottle.redirect("/main_page/")

#naredi isto kot pri vstopu v album, mogoce se en pripis da se pokaze?
# samo ce je username==album.owner   
@bottle.post("/add_to_album/<image_id>")
def add_to_album(image_id):
    account = current_account()
    album_name = bottle.request.forms.getunicode("album_name")
    album_owner = bottle.request.forms.getunicode("album_owner")
    album_id = album_name+"."+album_owner
    if album_id:
        Album(album_id).add_image(image_id)
    bottle.redirect("/main_page/") #izpis "**IMAGE** has been added to **ALBUM**"

@bottle.post("/album/<album_id>")
def enter_album(album_id):
    bottle.response.set_cookie("album", album_id, path="/", secret=CODE)
    bottle.redirect("/album/")

@bottle.get("/album/")
def albums(error=None):
    account = current_account()
    album = current_album()
    str_of_people = album.access_str()
    bottle.response.delete_cookie("image", path="/")
    return bottle.template("album.tpl", error=error, account=account, album=album, str_of_people = str_of_people)

@bottle.post("/add_friend/")
def add_friend():
    album = current_album()
    friend_name = bottle.request.forms.getunicode("friend")
    error = album.change_access(friend_name)
    if error:
        error = "Please enter your friends username."
    else:
        error = f"Your friend {friend_name} has been added to album."
    return albums(error)                              

@bottle.post("/image/<image_id>")
def enter_image(image_id):
    bottle.response.set_cookie("image", image_id, path="/", secret=CODE)
    bottle.redirect("/image/")

@bottle.get("/image/")
def images():
    account = current_account()
    image = current_image()
    return bottle.template("image.tpl", account=account, image=image)

@bottle.post("/like/")
def like_image():
    account = current_account()
    image = current_image()
    image.like(account)
    bottle.redirect("/image/")

@bottle.post("/dislike/")
def dislike_image():
    account = current_account()
    image = current_image()
    image.dislike(account)
    bottle.redirect("/image/")

@bottle.post("/add_comment/")
def add_comment():
    account = current_account()
    image = current_image()
    text = bottle.request.forms.getunicode("comment")
    image.add_comment(account, text)
    bottle.redirect("/image/")


@bottle.post("/log_out/")
def log_out():
    bottle.response.delete_cookie("account", path="/")
    bottle.response.delete_cookie("album", path="/")
    bottle.response.delete_cookie("image", path="/")
    bottle.redirect("/")





bottle.run(reloader=True, debug=True)
