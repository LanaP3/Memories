import bottle
import os
from model import *

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
        return bottle.template("login.tpl", note=note, error="Please enter your username and password. You may use numbers, lowercase and uppercase letters, as well as symbols:  _ * - and space.") 

@bottle.get("/")
def memories():
    bottle.redirect("/main_page/")

@bottle.get("/main_page/")
def main_page(error=None):
    account = current_account()
    list_of_albums = account.get_albums()
    note = current_note()
    if note == "new_album_error":
        error = "Please choose a name for your new album. You may use numbers, lowercase and uppercase letters, as well as symbols: _ * - and space."
        note = None
    elif note == "wrong ext":
        error = "Please only use '.png', '.jpg' and '.jpeg' file extensions."
        note = None
    bottle.response.delete_cookie("album", path="/")
    bottle.response.delete_cookie("image", path="/")
    bottle.response.delete_cookie("note", path="/")
    return bottle.template("main_page.tpl", account=account, list_of_albums=list_of_albums, note=note, error=error)

@bottle.post("/upload_image/")
def upload_image():
    account = current_account()
    upload = bottle.request.files.get('upload')
    new_photo = account.new_image(upload)
    if new_photo == "wrong ext":
        note = "wrong ext"
    elif new_photo == "old image":
        note = "You already have this photo in your gallery."
    else:
        new_photo
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
    if album_name and account.album_available(album_name):
        account.new_album(album_name)
        note = "You have successfully created a new album."
    else:
        note = "new_album_error"
    bottle.response.set_cookie("note", note, path="/", secret=CODE)
    bottle.redirect("/main_page/")

@bottle.post("/add_to_album/<image_id>")
def add_to_album(image_id):
    album_id = bottle.request.forms.get("album_id")
    if album_id == "":
        note = "Please choose an album."
    else:
        album = Album(album_id)
        if image_id in list(album.images):
            note = "This photo is already in the selected album. Do you want to add it to any of the other albums?"
        else:
            album.add_image(image_id)
            note = "You can now find this photo in your album."
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

@bottle.get("/image/<image_id>")
def enter_image(image_id):
    bottle.response.set_cookie("image", image_id, path="/", secret=CODE)
    bottle.redirect("/image/")

@bottle.get("/image/")
def images():
    account = current_account()
    image = current_image()
    return bottle.template("image.tpl", account=account, image=image)

@bottle.get("/delete_image/<image_id>")
def delete_image(image_id):
    album = current_album()
    Picture(image_id, album.id).delete()
    note = "Picture has been removed from your album."
    bottle.response.set_cookie("note", note, path="/", secret=CODE)
    bottle.redirect("/album/")

@bottle.get("/like/")
def like_image():
    account = current_account()
    image = current_image()
    image.like(account)
    bottle.redirect("/image/")

@bottle.get("/dislike/")
def dislike_image():
    account = current_account()
    image = current_image()
    image.dislike(account)
    bottle.redirect("/image/")

@bottle.post("/add_comment/")
def add_comment():
    account = current_account()
    image = current_image()
    text = check_grammar(bottle.request.forms.getunicode("comment"))
    if text != "":
        image.add_comment(account, text)
    bottle.redirect("/image/")

@bottle.post("/log_out/")
def log_out():
    bottle.response.delete_cookie("account", path="/")
    bottle.response.delete_cookie("album", path="/")
    bottle.response.delete_cookie("image", path="/")
    bottle.redirect("/")

bottle.run(reloader=True, debug=True)
