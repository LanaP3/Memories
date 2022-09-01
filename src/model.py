import datetime
import os
import json
import re

path_to_json = os.path.join(os.getcwd(),'..', "database", "data.json")
image_path = os.path.join(os.getcwd(),'..', "database")

def read_json():
    with open(path_to_json, "r") as json_file:
        data = json.load(json_file)
        return data

def write_json(data):
    with  open(path_to_json, "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


def check_grammar(word):
    if re.match("^[A-Za-z0-9_%+,*#-]*$", word): 
        return word
    return False

def sort_in_columns(list, n, i):
    '''returns elements of i-th colomn (starting at 0) if equally divided between n total columns'''
    x = len(list)//n
    m = len(list) - x*n
    start = i*x
    if i==m:
        start += i
        stop = start+x
    elif i<m+1:
        start += i
        stop = start+x+1
    else:
        start += m
        stop = start + x
    return list[start:stop]

class User:
    def __init__(self, username):
        data = read_json()
        self.username = username
        self.password = data[username]["password"]
        self.images = data[username]["images"]
        self.albums = data[self.username]["albums"] #slovar albumov... [Album(album_id) for album_id in data[username]["albums"]]

    def to_json(self):
        data = read_json()
        data[self.username]["password"] = self.password
        data[self.username]["images"] = self.images
        data[self.username]["albums"] = self.albums
        write_json(data)

    def correct_password(self, text):
        return self.password == text
    
    @staticmethod
    def find_account(username, password):
        data = read_json()
        for name in data:
            if username == name:
                if password == data[name]["password"]:
                    return name

    @staticmethod    
    def username_available(username):
        data = read_json()
        return username not in data

    @staticmethod
    def register(username, password):
        data = read_json()
        data[username] = {}
        data[username]["password"] = password
        data[username]["images"] = []
        data[username]["albums"] = {}
        write_json(data)

    def album_available(self, album_name):
        album_id = f'{album_name}.{self.username}'
        data = read_json()
        return album_id not in data[self.username]["albums"]        

    def new_album(self, album_name):
        self.albums[f"{album_name}.{self.username}"] = {
            "name": album_name,
            "owner": self.username,
            "date_added": str(datetime.date.today()),
            "access": [self.username],
            "images": {}
            }
        self.to_json()
    
    def new_image(self, upload):
        name, ext = os.path.splitext(upload.filename)
        image_id = f"{name}.{self.username}{ext}"
        save_path =  os.path.join(image_path, image_id)
        if ext not in ('.jpg', '.jpeg', '.png', '.JPG'):
            return "wrong ext"
        with open(save_path, "wb") as image_file:
            image_file.write(upload.file.read())
        
        data = read_json()
        if image_id in data[self.username]["images"]:    #image already saved
            return "old image"
        self.images.append(image_id)
        data[self.username]["images"].append(image_id)
        write_json(data)
    
    def get_albums_id(self):
        data = read_json()
        return list(data[self.username]["albums"])
    
    def get_albums(self):
        list_of_albums=[]
        for album_id in self.get_albums_id():
            list_of_albums.append(Album(album_id))
        return list_of_albums

    def num_friends_albums(self):
        n = 0
        for album in self.get_albums():
            if self.username != album.owner:
                n+=1
        return n

class Album:
    def __init__(self, album_id):
        data = read_json()
        self.id = album_id #oblike 'name.owner'
        self.name = album_id.split(".")[0]
        self.owner = album_id.split(".")[1]
        self.date_added = data[self.owner]["albums"][album_id]["date_added"]
        self.access = data[self.owner]["albums"][album_id]["access"]
        self.images = data[self.owner]["albums"][album_id]["images"]

    def to_json(self):
        data = read_json()
        for name in self.access:
            data[name]["albums"][self.id]["name"] = self.name
            data[name]["albums"][self.id]["owner"] = self.owner
            data[name]["albums"][self.id]["date_added"] = self.date_added
            data[name]["albums"][self.id]["access"] = self.access
            data[name]["albums"][self.id]["images"] = self.images
        write_json(data)

    def delete_album(self):
        data = read_json()
        for name in self.access:
            del data[name]["albums"][self.id]
        write_json(data)

    def leave_album(self, account):
        self.access.remove(account.username)
        self.to_json()
        del account.albums[self.id]
        account.to_json()

    def add_image(self, image_id):
        if image_id not in list(self.images):
            image_name = image_id.rsplit(sep=".", maxsplit=2)[2]
            self.images[image_id] = {
                "album_owner": self.owner,
                "name": image_name,
                "likes": [],
                "dislikes": [],
                "comments": []
                }
        self.to_json()

    def change_access(self, friend_name):
        data = read_json()
        if friend_name in data:
            if friend_name not in self.access:
                self.access.append(friend_name)
                friend = User(friend_name)
                friend.albums[self.id]={}
                friend.to_json()
                self.to_json()
                return False
        return True

    def access_str(self):
        s = ""
        for name in self.access:
            s += f", {name}"
        return s[2:]


class Picture:
    def __init__(self, image_id, album_id):
        data = read_json()
        album = Album(album_id)
        self.id = image_id #oblike 'name.owner.ext'
        self.album_owner = album.owner
        self.album_id = album_id
        self.name = image_id.rsplit(sep=".", maxsplit=2)[0] #lahko so v imenu slike '.'
        self.likes = data[self.album_owner]["albums"][album_id]["images"][image_id]["likes"]
        self.dislikes = data[self.album_owner]["albums"][album_id]["images"][image_id]["dislikes"]
        self.comments = data[self.album_owner]["albums"][album_id]["images"][image_id]["comments"]
    
    def to_json(self):
        album = Album(self.album_id)
        album.images[self.id]["album_owner"] = self.album_owner
        album.images[self.id]["name"] = self.name
        album.images[self.id]["likes"] = self.likes
        album.images[self.id]["dislikes"] = self.dislikes
        album.images[self.id]["comments"] = self.comments
        album.to_json()

    def delete(self):
        album = Album(self.album_id)
        del album.images[self.id]
        album.to_json()

    def add_comment(self, account, text):
        self.comments.append([account.username, text])
        self.to_json()

    def like(self, account):
        name = account.username
        if name in self.likes:
            self.likes.remove(name)
        elif name not in self. dislikes:
            self.likes.append(name)
        self.to_json()

    def dislike(self, account):
        name = account.username
        if name in self.dislikes:
            self.dislikes.remove(name)
        elif name not in self.likes:
            self.dislikes.append(name)
        self.to_json()

