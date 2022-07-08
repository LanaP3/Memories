from dataclasses import dataclass
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
            if password == data[user][password]:
                return user
def set_image_size():
    pass


class User:
    def __init__(self, username, password, images=[], albums=[]):
        self.username = username
        self.password = password
        self.images = images
        self.albums = albums
    
    def correct_password(self, text):
        return self.password == text

    @staticmethod
    def register(username, password):
        data = read_json()
        if username_available(data, username):
            new_user = User(username, password)
            data[username] = {"password":new_user.password, "images":new_user.images, "albums":new_user.albums}
            write_json(data)
        else:
            pass

    def album_available(self, album_name):
        data = read_json()
        return album_name not in data[self.username]["albums"]        

    def new_album(self, album_name):
        if self.album_available(album_name):
            new_album = Album(album_name)
            data = read_json()
            data[self.username]["albums"].append(new_album)
            write_json(data)
    
    def new_image(self, upload):
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
        data[image_id] = {"owner": user, "likes" : 0, "image_name": f"{name}_{user}", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext, "labels" : []}
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
    date_added: date
    owner: User
    name: str
    access: List[User]
    images: List[Image]

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

    def change_access(self, user, username): 
        if user == self.owner:
            data = read_json()
            data[self.owner][self.owner.albums][self.name]["access"].append(username)
            write_json(data)
        else:
            pass





