from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from app.models import Image
from app.forms import ImageForm, CommentForm
from datetime import date
import MySQLdb
from PIL import Image
from django import forms

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {'form': form})

#Retrieve list of usernames from database table to populate the user index page with hyperlinks to user profiles
def listUsers(request):
	dbconnect = MySQLdb.connect('localhost', 'djangouser', 'password', 'test_data')
	cursor = dbconnect.cursor()
	cursor.execute('SELECT * FROM `auth_user`;')
	usernames = cursor.fetchall()
	dbconnect.close()
	return render(request, 'app/userlist.html', {'usernames': usernames})

def profile(request, username):
	if request.user.username == username:
		return myProfile(request)
	else:
		dbconnect = MySQLdb.connect('localhost', 'djangouser', 'password', 'test_data')
		cursor = dbconnect.cursor()
		cursor.execute('SELECT * FROM `app_image` WHERE username = %s;', [username])
		images = cursor.fetchall()
		dbconnect.close()
		return render(request, 'app/users/profile.html', {'username': username, 'images': images})
		
def myProfile(request):
	dbconnect = MySQLdb.connect('localhost', 'djangouser', 'password', 'test_data')
	cursor = dbconnect.cursor()
	cursor.execute('SELECT * FROM `app_image` WHERE username = %s;', [request.user.username])
	images = cursor.fetchall()
	dbconnect.close()
	return render (request, 'app/myprofile.html', {'images': images})

def imageView(request, image_id):
	
	dbconnect = MySQLdb.connect('localhost', 'djangouser', 'password', 'test_data')
	cursor = dbconnect.cursor()
	cursor.execute('SELECT * FROM `app_image` WHERE id = %s;', [image_id])
	image_info = cursor.fetchone()
	cursor.execute('SELECT * FROM `app_comment` WHERE parent_image = %s;', [image_id])
	comments = cursor.fetchall()
	dbconnect.close()
	return render (request, 'app/images/image.html', {'image_info': image_info, 'comments':comments})

def uploadView(request):
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return myProfile(request)
	else:
		form = ImageForm()
		form.fields['username'].widget = forms.HiddenInput()
		form.fields['username'].initial = request.user.username
		form.fields['posted_on'].widget = forms.HiddenInput()
		form.fields['posted_on'].initial = date.today()
	return render(request, 'app/upload.html', {'form' : form})

def allImages(request):
	dbconnect = MySQLdb.connect('localhost', 'djangouser', 'password', 'test_data')
	cursor = dbconnect.cursor()
	cursor.execute('SELECT * FROM `app_image`')
	images = cursor.fetchall()
	dbconnect.close()
	return render (request, 'app/images/allimages.html', {'images': images})

def addComment(request):
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('my_profile')
	else:
		imageurl = request.META.get('HTTP_REFERER')
		form = CommentForm()
		form.fields['parent_image'].widget = forms.HiddenInput()
		form.fields['parent_image'].initial = int(imageurl.split('/')[-1])
		form.fields['username'].widget = forms.HiddenInput()
		form.fields['username'].initial = request.user.username
		form.fields['posted_on'].widget = forms.HiddenInput()
		form.fields['posted_on'].initial = date.today()
		return render (request, 'app/addcomment.html', {'form': form})
