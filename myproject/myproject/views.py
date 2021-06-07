from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from app.models import Image
from app.forms import ImageForm
from datetime import datetime
import MySQLdb

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			#Custom database stuff here
			dbconnect = MYSQLdb.connect('localhost', 'root', 'password', 'app_data')
			cursor = dbconnect.cursor()
			sql = 'INSERT INTO users (username, created_at) VALUES (%s, %s);'
			val = (username, datetime.now())
			cursor.execute(sql, val)
			dbconnect.close
			#End custom db stuff
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {'form': form})

#Retrieve list of usernames from database table to populate the user index page with hyperlinks to user profiles
def listUsers(request):
	dbconnect = MySQLdb.connect('localhost', 'root', 'password', 'app_data')
	cursor = dbconnect.cursor()
	cursor.execute('SELECT * FROM `users`;')
	usernames = cursor.fetchall()
	for username in usernames:
		print(username[0])
	dbconnect.close()

	return render(request, 'app/userlist.html', {'usernames': usernames})

def profile(request, username):
	if request.user.username == username:
		return myProfile(request)
	else:
		dbconnect = MySQLdb.connect('localhost', 'root', 'password', 'app_data')
		cursor = dbconnect.cursor()
		cursor.execute('SELECT image_data FROM `images` WHERE user_id = %s;', [username])
		images = cursor.fetchall()
		dbconnect.close()
		return render(request, 'app/users/profile.html', {'username': username, 'images': images})
		
def myProfile(request):
	dbconnect = MySQLdb.connect('localhost', 'root', 'password', 'app_data')
	cursor = dbconnect.cursor()
	cursor.execute('SELECT image_data FROM `images` WHERE user_id = %s;', [request.user.username])
	images = cursor.fetchall()
	dbconnect.close()
	return render (request, 'app/myprofile.html', {'images': images})

def imageView(request, image_id):
	dbconnect = MySQLdb.connect('localhost', 'root', 'password', 'app_data')
	cursor = dbconnect.cursor()
	cursor.execute('SELECT * FROM `images` WHERE image_id = %s;', [image_id])
	image_info = cursor.fetchone()
	cursor.execute('SELECT * FROM `comments` WHERE image_id = %s;', [image id])
	comments = cursor.fetchall()
	dbconnect.close()
	return render (request, 'app/images/image.html', {'image_info': image_info, 'comments': comments})

def uploadView(request):
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		#if form.is_valid(): #I should really fix this but PIL refuses to be imported
		#dbconnect = MYSQLdb.connect('localhost', 'root', 'password', 'app_data')
		#cursor = dbconnect.cursor()
		#sql = 'INSERT INTO images (caption, posted_at, user_id, image_data) VALUES (%s, %s, %s, %s);'
		#val = (form.caption, datetime.now(), request.user.username, form.image)
		#cursor.execute(sql, val)
		#dbconnect.close
		return myProfile(request)
	else:
		form = ImageForm()
	return render(request, 'app/upload.html', {'form' : form})

def allImages(request):
	dbconnect = MySQLdb.connect('localhost', 'root', 'password', 'app_data')
	cursor = dbconnect.cursor()
	cursor.execute('SELECT * FROM `images`')
	image_info = cursor.fetchall()
	dbconnect.close()
	return render (request, 'app/images/allimages.html', {'image_info': image_info})
