from django.db import models
from datetime import datetime
from django.utils.baseconv import base56
from random import randint
from django.contrib.auth.models import User

# Create your models here.

def random_key():
    return base56.encode(randint(0, 0x7fffff))

class Picture(models.Model):
    image = models.ImageField(default = 'pic_folder/None/no-img.jpg')
    description = models.CharField(max_length=100, default='')
    key = models.SlugField(max_length=10, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_view = models.DateTimeField(null=True, auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    #likes_count = models.PositiveIntegerField(default=0)
    user = models.CharField(max_length=20, default='anonymous')
    #auth_user = models.OneToOneField(User)

    def __str__(self):
        return self.key + ' : ' +str(self.image)
        
    @classmethod
    def create(cls, image, user, description=''):
        created = False
        while created == False:
            key = random_key()
            obj, created = cls.objects.get_or_create(key=key, defaults={'image': image, 'description': description, 'user': user})
        #l = Like.objects.create(id=obj.id)
        return obj

#    def delete(self, key):
#        instance = Picture.objects.get(key=key)
#        instance.delete()
#        return 0

#   def view(self, key):
#       instance = Picture.objects.get(key=key)
#       return instance

    def get_absolute_url(self):
        #зачем нужен, и что должен делать
        pass
        
class Like(models.Model):
    id = models.OneToOneField(Picture, primary_key=True)
    likes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        #p = Picture.objects.get(id=self)
        return str(self.id)# + ' : ' + str(p.key)