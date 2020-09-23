from django.db import models

# Create your models here.
#Track will be a table in the database and title, description,url, created_at will be columns of the table.

class Track(models.Model):
    #id will be automatically be created by django.
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True) #description can be None.
    url = models.URLField()  #url to access the track
    created_at = models.DateTimeField(auto_now_add=True) #auto_now_add uses current date and time.