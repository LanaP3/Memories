class Album:
    def __init__(self, ime, images, public=False):
        self.ime = ime
        self.images = images
        self.public = public

    def download(self):
        pass

    def add_image(self):
        pass

    def change_access(self):
        pass

    
class Image:
    def __init__(self, ime, ranking, comments):
        self.ime = ime
        self.ranking = ranking
        self.comments = comments

    def download(self):
        pass

    def add_comment(self):
        pass

    def rate(self):
        pass


#class Comment:
#    def __init__(self, text):
#        self.text = text

