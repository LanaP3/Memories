from datetime import date

class Album:
    def __init__(self, date, ime, images, public=False):
        self.date = date.today()
        self.ime = ime
        self.images = images
        self.public = public

    def download(self):
        pass

    def add_image(self):
        pass

    def make_public(self):
        self.public = True

    def make_private(self):
        self.public = False


class Image:
    def __init__(self, date, ime, likes, dislikes, comments):
        self.date = date.today()
        self.ime = ime
        self.likes = likes
        self.dislikes = dislikes
        self.comments = comments

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


class Comment:
    def __init__(self, date, comment):
        self.date = date.today()
        self.comment = comment

