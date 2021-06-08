from django.db import models
from django import forms

class Image(models.Model):
	image = models.ImageField(blank=False)
	caption = models.CharField(blank=False, max_length=500)
	username = models.CharField(max_length=128)
	posted_on = models.DateField()
	
class Comment(models.Model):
	comment_text = models.CharField(max_length=200)
	parent_image = models.IntegerField()
	username = models.CharField(max_length=128)
	posted_on = models.DateField()

