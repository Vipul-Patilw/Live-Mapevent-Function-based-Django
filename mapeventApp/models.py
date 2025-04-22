
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.
class Login(models.Model):
	
	first_name = models.CharField(max_length=122)
	
	last_name = models.CharField(max_length=122)
	
	mobile_number= models.CharField(max_length=122)
	
	username= models.CharField(max_length=122)
		
	email= models.CharField(max_length=122)

	password= models.CharField(max_length=122)
	
	gender = models.CharField(max_length=122)

	birthdate = models.DateField()

	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

	profile_pic = models.ImageField(upload_to= "users_profile",blank=True)

	def __str__(self):
		return self.first_name

class Staff(models.Model):
	
	first_name = models.CharField(max_length=122)
	
	last_name = models.CharField(max_length=122)
	
	username= models.CharField(max_length=122)
		
	email= models.CharField(max_length=122)

	password= models.CharField(max_length=122)
		
	def __str__(self):
		return self.first_name 


class Sign(models.Model):
	username  = models.CharField(max_length=122)
	Loginpassword = models.CharField(max_length=122)
	def __str__(self):
		return self.username

class ChangePassword(models.Model):
		old_password = models.CharField(max_length=122)
		new_password1= models.CharField(max_length=122)
		newpassword2 = models.CharField(max_length=122)


class Event(models.Model):
		event = models.CharField(max_length=122)
		eventaddress = models.TextField()
		dtime = models.CharField(max_length=122)
		full_name = models.CharField(max_length=122)
		email = models.CharField(max_length=122)
		emailowner = models.CharField(max_length=122)
		mobile_number = models.CharField(max_length=122)
		date = models.DateField()
		time = models.TimeField()

		def __str__(self):
			return self.event 
		
class Add(models.Model):
		event = models.CharField(max_length=122)
		box = models.CharField(max_length=122)
		
		def __str__(self):
			return self.event 	
class AddEvent(models.Model):
		event = models.CharField(max_length=122)
		info = models.TextField()
		eventaddress = models.TextField()
		fromdate = models.DateField(max_length=122)
		todate= models.DateField(max_length=122)
		fromtime = models.TimeField()
		totime= models.TimeField()
		lat = models.CharField(max_length=122)
		lang = models.CharField(max_length=122,default='')
		icon = models.CharField(max_length=122)
		location = models.CharField(max_length=122,default='')
		eventermail = models.CharField(max_length=122,default='bankpay980@gmail.com')
		city = models.CharField(max_length=122,default='pune')
		locate = models.CharField(max_length=122,default='dadar')
		event_poster = models.ImageField(upload_to= "event_posters",blank=True)
		

		def __str__(self):
			return self.city
		objects = models.Manager()
class LocateEvent(models.Model):
		lat = models.CharField(max_length=122)
		lang = models.CharField(max_length=122,default='')			
class ForgotPassword(models.Model):
	email = models.CharField(max_length=222)
