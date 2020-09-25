from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
#Track will be a table in the database and title, description,url, created_at will be columns of the table.

class Track(models.Model):
    #id will be automatically be created by django.
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True) #description can be None.
    url = models.URLField()  #url to access the track
    created_at = models.DateTimeField(auto_now_add=True) #auto_now_add uses current date and time.
    posted_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)  #foreign key
    track = models.ForeignKey('tracks.Track',related_name='likes',on_delete=models.CASCADE) #foreign key
