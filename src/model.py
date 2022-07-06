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


class User:
    #def __init__(username, password):
    #    if False:
    #        pass
    #    else:
    #        raise Exception as "Username not available"
    def correct_password(self, text):
        return self.password == text

    #def find_user(self, username, password):
    #    for user in self.users:
    #        if user.username == username:
    #            if user.correct_password(password):
    #                return user

@dataclass
class Comment:
    date_added: date
    comment: str

    def delete(self):
        pass

@dataclass
class Image:
    date_added: date
    name: str
    likes: int
    dislikes: int
    comments: List[Comment]
    
    def delete(self):
        pass

    def download(self):
        pass

    def add_comment(self, comment):
        self.comments.append(comment)

    def like(self):
        self.likes += 1

    def dislike(self):
        self.dislikes += 1

    def rating(self):
        if self.likes+self.dislikes == 0:
            return None
        else:
            return ((self.likes-self.dislikes)/(self.likes+self.dislikes) * 5) + 5
@dataclass
class Album:
    date_added: date
    owner: User
    name: str
    access: List[User]
    images: List[Image]

    def delete(self):
        pass

    def download(self):
        pass

    def add_image(self):
        pass

    def change_access(self): #only possible by owner
        pass

    def sort(self):
        pass




