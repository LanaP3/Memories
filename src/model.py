from dataclasses import dataclass
import datetime
from datetime import date
from typing import List
from PIL import Image, ImageFilter
import os
import json
import re

path_to_json = os.path.join(os.getcwd(),'..', "database", "data.json")
picture_path = os.path.join(os.getcwd(),'..', "database")

def read_json():
    with open(path_to_json, "r") as json_file:
        data = json.load(json_file)
        return data

def write_json(data):
    with  open(path_to_json, "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)



def username_available(data, username):
    return username not in data


def find_user(data, username, password):
    for user in data:
        if username == user:
            if password == data[user]["password"]:
                return user

def set_image_size():
    pass


class User:
    def __init__(self, username):
        data = read_json()
        self.username = username
        self.password = data[username]["password"]
        self.images = data[username]["images"]
        self.albums = [Album(album, self.username) for album in data[username]["albums"]]
    
    def correct_password(self, text):
        return self.password == text

    @staticmethod
    def register(username, password):
        data = read_json()
        data[username] = {}
        data[username]["password"] = password
        data[username]["images"] = []
        data[username]["albums"] = []
        write_json(data)

    def album_available(self, album_name):
        data = read_json()
        return album_name not in data[self.username]["albums"]        

    def new_album(self, album_name):
        if self.album_available(album_name):
            new_album = Album(album_name, self.username)
            data = read_json()
            data[self.username]["albums"].append(album_name)
            data[self.username]["albums"][album_name]["owner"] = new_album.owner
            data[self.username]["albums"][album_name]["access"] = new_album.access
            data[self.username]["albums"][album_name]["date_added"] = new_album.date_added
            data[self.username]["albums"][album_name]["images"] = new_album.images
            write_json(data)
    
    def new_image(self, upload, image_name):
        name, ext = os.path.splitext(upload.filename)
        image_id = f"{name}_{self.username}"
        image_path =  os.path.join(image_path, image_id + f"{ext}")
        if ext not in ('.jpg', '.jpeg', '.png'):
            return "Please only use '.jpeg', '.jpg' or '.png' file extensions."
        with open(image_path, "wb") as image_file:
            image_file.write(upload.file.read())
        set_image_size(image_path, 800)
        
        data = read_json()
        if image_id in data["all_images"]:    #image already saved
            return None
        data[image_id] = {"owner": self.username, "likes" : 0, "image_name": f"{name}_{self.username}", "dislikes" : 0, "comments" : [], "date": datetime.date.today().__str__(), "ext": ext, "labels" : []}
        write_json(data)
    
    def get_albums(self):
        data = read_json()
        return data[self.username]["albums"]


@dataclass
class Image:
    date_added: date
    owner: User
    name: str
    likes: int
    dislikes: int
    comments: list
    
    def delete(self, album, user):
        if user == self.owner:
            data = read_json()
            del data[self.owner][self.owner.albums]["album"]["images"][self.name]
            write_json(data)
        else:
            pass

    def download(self):
        pass

    def add_comment(self, album, comment):
        data = read_json()
        data[self.owner][self.owner.albums]["album"]["images"][self.name]["comments"].append(comment)
        write_json(data)

    def like(self,album):
        data = read_json()
        data[self.owner][self.owner.albums]["album"]["images"][self.name]["likes"] += 1
        write_json(data)

    def dislike(self,album):
        data = read_json()
        data[self.owner][self.owner.albums]["album"]["images"][self.name]["dislikes"] += 1
        write_json(data)

    #def rating(self):
    #    if self.likes+self.dislikes == 0:
    #        return None
    #    else:
    #        return ((self.likes-self.dislikes)/(self.likes+self.dislikes) * 5) + 5

@dataclass
class Album:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.date_added = datetime.date.today()
        self.access = [owner]
        self.images = []

    def delete(self, user):
        if user == self.owner:
            data = read_json()
            del data[self.owner][self.owner.albums][self.name]
            write_json(data) 
        else:
            pass

    def download(self):
        pass

    def add_image(self, image):
        data = read_json()
        data[self.owner][self.owner.albums][self.name]["images"].append(image)
        write_json(data)

    def change_access(self, user, friend): 
        if user == self.owner:
            data = read_json()
            data[self.owner][self.owner.albums][self.name]["access"].append(friend)
            write_json(data)
        else:
            pass





