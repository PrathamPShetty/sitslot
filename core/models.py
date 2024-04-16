from django.db import models

from datetime import datetime
from django.contrib.auth.models import User



class places(models.Model):
    name = models.CharField(max_length=100)
    images = models.ImageField(upload_to='place_photo')
    img1 = models.ImageField(upload_to='place_photo',default='', null=True, blank=True)
    img2 = models.ImageField(upload_to='place_photo',default='', null=True, blank=True)
    img3 = models.ImageField(upload_to='place_photo',default='', null=True, blank=True)
    img4 = models.ImageField(upload_to='place_photo',default='', null=True, blank=True)
    img5 = models.ImageField(upload_to='place_photo',default='', null=True, blank=True)
    introduction = models.CharField(max_length=1000,default='', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name



class Event(models.Model):
    email = models.EmailField()
    event = models.CharField(max_length=100)
    date = models.DateField(default=datetime(1970, 1, 1))
    start_time = models.DateTimeField(default=datetime(1970, 1, 1))
    end_time = models.DateTimeField(default=datetime(1970, 1, 1))
    image = models.ImageField(upload_to='image')
    place = models.ForeignKey(places, on_delete=models.CASCADE)
    discription = models.CharField(max_length=1000,default='', null=True, blank=True)
    location= models.CharField(max_length=20,default='', null=True, blank=True)
    myuser = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    

class display(models.Model):
    program = models.ForeignKey(Event, on_delete=models.CASCADE)
    
