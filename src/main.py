from attr import define
import bottle
import os
import sys
from bottle import get, post, request
from datetime import datetime
from model import *
#te pripise, errorje bi lahko dala da se vsi na istem mestu vedno izpisejo, npr. okvircek desno zgoraj
#dodaj ikonce
#drop-down seznam za izbiro albuma in creatorja
#lepsa forma za uploadanje slik
#da vstopis v sliko kar s klikom nanjo
#komentarje, izpisejo se v vsakem primeru, ce jih se ni, nekaj v smislu: "no comments yet"

path_to_code = os.path.join(os.getcwd(),'..', "database", "secret.txt")
with open(path_to_code, "r") as d:
    CODE = d.read()

app = bottle.default_app()
bottle.BaseTemplate.defaults['get_url'] = app.get_url

def current_note():
    note = bottle.request.get_cookie("note", secret=CODE)
    return note

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
    note = "If you already have an account, enter your username and password. If you are new here, just choose a username and password, then click REGISTER."
    bottle.response.set_cookie("note", note, path="/", secret=CODE)
    return bottle.template("login.tpl", note = note, error=None)

@bottle.post("/log_in/")
def do_login():
    note = current_note()
    username = bottle.request.forms.getunicode("username")
    password = bottle.request.forms.getunicode("password")
    if username and password:
        if User.find_account(username, password):
            bottle.response.set_cookie("account", username, path="/", secret=CODE)
            note = f"Welcome back {username}!"
            bottle.response.set_cookie("note", note, path="/", secret=CODE)
            bottle.redirect("/")
        else:
            return bottle.template("login.tpl", note=note, error="Your password is incorrect.")
    else:
        return bottle.template("login.tpl", note=note, error="Please enter your username and password.")        

@bottle.post("/register/")
def register():
    note = current_note()
    username = check_grammar(bottle.request.forms.getunicode("username"))
    password = check_grammar(bottle.request.forms.getunicode("password"))
    if username and password:
        if User.username_available(username):
            User.register(username, password)
            bottle.response.set_cookie("account", username, path="/", secret=CODE)
            note = "Welcome to MEMORIES! To start, first upload a photo or create new album."
            bottle.response.set_cookie("note", note, path="/", secret=CODE)
            bottle.redirect("/")
        else:
            return bottle.template("login.tpl", note=note, error="This username is already taken. Please choose another one.")             
    else:
        return bottle.template("login.tpl", note=note, error="Please enter your username and password. You may use numbers, lowercase and uppercase letters as well as symbols: _ % + * , # -") 

@bottle.get("/")
def memories():
    bottle.redirect("/main_page/")

@bottle.get("/main_page/")
def main_page(error=None):
    account = current_account()
    list_of_albums = account.get_albums()
    note = current_note()
    if note == "new_album_error":
        error = "Please choose name for your new album. You may use numbers, lowercase and uppercase letters as well as symbols: _ % + * , # -"
        note = None
    elif note == "add_to_album_missing":
        error = "Enter album name as well as album creator."
        note = "To which album do you want to add this photo?"
    elif note == "add_to_album_info":
        note = None
        error = "Album info is incorrect."
    bottle.response.delete_cookie("album", path="/")
    bottle.response.delete_cookie("image", path="/")
    bottle.response.delete_cookie("note", path="/")
    return bottle.template("main_page.tpl", account=account, list_of_albums=list_of_albums, note=note, error=error)

@bottle.post("/upload_image/")
def upload_image():
    account = current_account()
    upload = bottle.request.files.get('upload')
    account.new_image(upload)    
    if account.albums == {}:
        note = "That is a nice photo! Now create a new album and you can add the photo to it."
    else:
        note = "That is a nice photo! You can now add it to any of your albums. Just enter album info and submit."
    bottle.response.set_cookie("note", note, path="/", secret=CODE)
    bottle.redirect("/main_page/")

@bottle.post("/new_album/")
def create_new_album():
    account = current_account()
    album_name = check_grammar(bottle.request.forms.getunicode("new_album"))
    if album_name:
        account.new_album(album_name)
        note = "You have successfully created a new album."
    else:
        note = "new_album_error"
    bottle.response.set_cookie("note", note, path="/", secret=CODE)
    bottle.redirect("/main_page/")

@bottle.post("/add_to_album/<image_id>")
def add_to_album(image_id):
    data = read_json()
    account = current_account()
    album_name = check_grammar(bottle.request.forms.getunicode("album_name"))
    album_owner = check_grammar(bottle.request.forms.getunicode("album_owner"))
    if album_owner and album_name:
        note = "add_to_album_info"
        if album_owner in data:
            album_id = album_name+"."+album_owner
            if album_id in User(album_owner).albums:
                if image_id in list(Album(album_id).images):
                    note = "This photo is already in selected album. Do you want to add it to any of the other albums?"
                else:
                    Album(album_id).add_image(image_id)
                    note = "You can now find this photo in your album."
    else:
        note = "add_to_album_missing"
    bottle.response.set_cookie("note", note, path="/", secret=CODE)
    bottle.redirect("/main_page/")

@bottle.post("/album/<album_id>")
def enter_album(album_id):
    bottle.response.delete_cookie("image", path="/")
    bottle.response.set_cookie("album", album_id, path="/", secret=CODE)
    bottle.redirect("/album/")

@bottle.get("/album/")
def albums():
    account = current_account()
    album = current_album()
    note = current_note()
    if note == "add_friend_failed":
        note = None
        error = "Please enter your friends username."
    else:
        error = None
    str_of_people = album.access_str()
    bottle.response.delete_cookie("image", path="/")
    bottle.response.delete_cookie("note", path="/")
    return bottle.template("album.tpl", note=note, error=error, account=account, album=album, str_of_people=str_of_people)

@bottle.post("/add_friend/")
def add_friend():
    album = current_album()
    friend_name = check_grammar(bottle.request.forms.getunicode("friend"))
    error = album.change_access(friend_name)
    if error:
        note = "add_friend_failed"
    else:
        note = f"Your friend {friend_name} has been added to album."
    bottle.response.set_cookie("note", note, path="/", secret=CODE)
    bottle.redirect("/album/")

@bottle.post("/remove_album/")
def remove_album():
    account = current_account()
    album = current_album()
    if account.username == album.owner:
        album.delete_album()
        note = "You have just deleted your album."
    else:
        album.leave_album(account)
        note = "You have left the album group. If you later change your mind, you can just ask the album creator to add you again."
    bottle.response.set_cookie("note", note, path="/", secret=CODE)
    bottle.redirect("/main_page/")                              

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
