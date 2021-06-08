from django import forms
from .models import *
from datetime import datetime

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ['image', 'caption', 'username', 'posted_on']
		#widgets = {'username': forms.HiddenInput}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment_text', 'parent_image', 'username', 'posted_on']
