#pylint:disable=E0602
#pylint:disable=E0001
from quopri import decodestring
from django.shortcuts import redirect, render
from django.core.paginator import  Paginator
from mapeventApp.models import  Event, Login,ForgotPassword,Staff,Add
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
import re
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from mapeventProject import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from . tokens import generate_token
from django.core.mail import EmailMessage
from .models import AddEvent
import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from django.shortcuts import render, redirect 
from django.conf import settings
from django.core.files.storage import FileSystemStorage
 
import csv
def import_export_event_csv(request):
 
    if 'export_event' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="EventsData.csv"'        
        writer = csv.writer(response)
        
        writer.writerow(['Event Details'])
        writer.writerow(['Event Name','Event Address' , 'Event Detail' , 'Event from date','Event till date','Event from time','Event till time','City','lat','lang','icon'])
 
        events = AddEvent.objects.all().values_list('event','eventaddress' , 'info' , 'fromdate','todate','fromtime','totime','city','lat','lang','icon' )
        for event in events:
            writer.writerow(event)
        return response
              
    try:
        if request.method =="POST" and request.FILES['myfile']:
            myfile = request.FILES['myfile']    
          
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_excel("."+excel_file)
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                fromtime = dbframe.time_from
                fromdate = dbframe.event_datefrom
                todate = dbframe.event_datetill
                obj = AddEvent.objects.create(event=dbframe.event_name,info=dbframe.event_details, eventaddress=dbframe.event_address,fromdate=fromdate,todate=todate,lat=dbframe.latitude,lang=dbframe.longitude,icon=dbframe.event_icon,city=dbframe.city,fromtime=fromtime,totime= dbframe.time_till)
                print(type(obj))
                obj.save()
 
            return redirect('/map')
    except Exception as identifier:
        messages.error(request,f"{identifier}")
        return redirect('/importexportevent')
     
    return render(request, 'importexportevent.html',{})
 
# Create your views here.

class changePassword(PasswordChangeView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('password_success')

def password_success(request):
	messages.info(request,"Password Changed Successfully")
	return render (request, 'personalDetails.html')


def index(request):
	try:
		if request.method =="POST":
		
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			mobile_number= request.POST.get('mobile_number')
			username= request.POST.get('username')
			email = request.POST.get('email')
			password= request.POST.get('password')
			gender = request.POST.get('gender')
			birthdate = request.POST.get('birthdate')
			password2 = request.POST.get('password2')
			
		
			if User.objects.filter(email=email):
						messages.error(request,"this email address already registered with us try different email address")
						return redirect("/sign")
						
			if User.objects.filter(username=username):
						messages.error(request,"this username is already exist try another")
						return redirect("/sign")

			if password != password2:
				messages.error(request,"confirm password doesn't matched with the password")
				return redirect ('/sign')
				
			if len(password)>=8 and re.search(r"[A-Z]",password) and re.search(r"[a-z]",password) and re.search(r"[@_!#$%^&*()?/}{~:]",password)and re.search(r"[0-9]",password):
				pass
				
			else:
				messages.error(request,"password should be at least 6 character long. contain both uppercase and lowercase character, at least one alpha numeric and one special charecter  (eg:Test@123)")
				return redirect("/sign")
				

			messages.success(request, first_name.title() + " " + last_name.title())
			myuser = User.objects.create_user(username,email,password)
			myuser.first_name = first_name
			myuser.last_name = last_name
			myuser.is_active = True
			myuser.save()	
			
			users = Login(first_name=first_name,username=username, mobile_number=mobile_number,last_name=last_name,email=email,birthdate=birthdate,gender=gender,)
			users.save()		
			
			#confirmation email
			current_site = get_current_site(request)
			email_sub2 = 'Activate your MCCIA Account'
			message2 = render_to_string('email_confirmation.html',{
				'fname': myuser.first_name,
				'lname': myuser.last_name, 
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
				'token': generate_token.make_token(myuser)
				})
			email = EmailMessage(
				email_sub2,
				message2,
				settings.EMAIL_HOST_USER,
				[myuser.email],
				)
			
			email.fail_silently= True
			email.send()

			
			return render(request, 'gotologin.html')

		#	except:
			#	messages.error(request,"some problem come in our application please reopen the application")
			#	return redirect ('/sign')
				
		#return render(request, 'logininfo.html')	
		return render(request, 'logininfo.html')
	except:
		messages.error(request,"since google disabled the smpt from 30may2022 we are not able to send mail.So you don't need confirmation link we activate your account you can login now")
		return redirect('/gotologin')
	
	#  return HttpResponse("vipul patil")
def adminsign(request):
		if request.method =="POST":
		
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			username= request.POST.get('username')
			email = request.POST.get('email')
			password= request.POST.get('password')
			password2 = request.POST.get('password2')
					
			if User.objects.filter(email=email):
						messages.error(request,"this email address already registered with us try different email address")
						return redirect("/adminsignIn")
						
			if User.objects.filter(username=username):
						messages.error(request,"this username is already exist try another")
						return redirect("/adminsignIn")

			if password != password2:
				messages.error(request,"confirm password doesn't matched with the password")
				return redirect ('/adminsignIn')
				
			if len(password)>=8 and re.search(r"[A-Z]",password) and re.search(r"[a-z]",password) and re.search(r"[@_!#$%^&*()?/}{~:]+[0-9]",password):
				pass
				
			else:
				messages.error(request,"password should be at least 6 character long. contain both uppercase and lowercase character, at least one alpha numeric and one special charecter  (eg:Test@123)")
				return redirect("/adminsignIn")
			messages.success(request, first_name.title() + " " + last_name.title())
			myuser = User.objects.create_user(username,email,password)
			myuser.first_name = first_name
			myuser.last_name = last_name
			myuser.is_active = False
			myuser.save()	
			users = Staff(first_name=first_name,username=username, last_name=last_name,email=email)
			users.save()			
			return render(request, 'gotologinadmin.html')
	
		#	except:
			#	messages.error(request,"some problem come in our application please reopen the application")
			#	return redirect ('/sign')
				
		#return render(request, 'logininfo.html')	
		return render(request, 'adminsignIn.html')

def gotologin(request):
	return render (request,'gotologin.html')	
def sign(request):

	if request.method =="POST":
		Loginpassword= request.POST.get('Loginpassword')
		username = request.POST.get('username')
		user = authenticate(username=username, password=Loginpassword)
		if user is not None:
			
			login(request, user)
			return redirect('/map')
			#full_name = user.first_name	
		else:
	#	if str(Loginpassword) == str(b):
		#	messages.error(request,"password matched")
		#	return redirect('/login')    				 
			messages.error(request, "Please enter correct username and  password ")
			return redirect('/login')    
		#	return render(request,'index.html')   
	return render(request,'index.html')


def adminlogin(request):
	try:
		if request.method =="POST":
			Loginpassword= request.POST.get('Loginpassword')
			username = request.POST.get('username')
			user = authenticate(username=username, password=Loginpassword)
			
			if user is not None and user.is_superuser == True or user.is_staff == True:
				
				login(request, user)
				return redirect('/map')
				#full_name = user.first_name
			
			elif user.is_staff == False or user.is_superuser == False:
					messages.error(request, "this account don't have accessed to login as admin or staff, try using your admin or staff login account!")
						
					return redirect('/adminlogin')
			
			#	return render(request,'index.html')   
		return render(request,'Adminlogin.html')
	except:
				messages.error(request, "You enter wrong username and password")
					
				return redirect('/adminlogin')    

	
def setting(request):
	return render (request,'setting.html')
		
def personalDetails (request):
	return render (request,'personalDetails.html')

def logoutuser(request):
	logout(request)
	return redirect ("/login")

def activate(request, uidb64, token):

	uid = decodestring(urlsafe_base64_decode(uidb64))
	myuser = User.objects.get(pk=uid)


	if myuser is not None and generate_token.check_token(myuser, token):
		myuser.is_active = True
		myuser.save()
		login(request,myuser)
		return redirect('/login')
		
	else:
		return render(request, 'activation_failed.html')	
			
#def location (request):
#			if request.method =="POST":
#				mumbai= request.POST.get('mumbai')
#				geolocator = Nominatim(user_agent="MyApp")
#				location = geolocator.geocode(mumbai)
#				lang = location.longitude
#				lat = location.latitude
#				return render(request,'searchDetail.html',{'lat':lat,'lang':lang})
#			return render(request,'deleteevent.html')
							
def searchDetail(request):
	return render (request,'searchDetail.html')
		
def forgotpassword(request):
	try:
		if request.method =="POST":
			email = request.POST.get('email')
			user = ForgotPassword(email=email)
			user.save()
			myuser = User.objects.get(email=email)
			current_site = get_current_site(request)
			email_sub2 = 'Reset Your MCCIA Account Password'
			body = render_to_string('password_resetMail.html',{
					'fname': myuser.first_name,
					'lname': myuser.last_name, 
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
					'token': generate_token.make_token(myuser)
					})
			email = EmailMessage(
					email_sub2,
					body,
					settings.EMAIL_HOST_USER,
					[myuser.email],
					)
				
			email.fail_silently= True
			email.send()

			messages.info(request,"Link of recovery password has been sent to your Email address please click that link in order to change your password")
			return render(request,'forgotPassword.html')
			
		return render(request,'forgotPassword.html')
	except:
		messages.error(request,"Sorry! this email address is not registered with us")
		return render(request,'forgotPassword.html')

def resetpasswordlink(request, uidb64, token):
	uid = decodestring(urlsafe_base64_decode(uidb64))
	myuser = User.objects.get(pk=uid)
	if myuser is not None and generate_token.check_token(myuser, token):
		login(request,myuser)
		return redirect('/reset_password_success')
		
	else:
		return render(request, 'password_reset_failed.html')
	
def reset_password_success(request):
	if request.method =="POST":
		email = request.POST.get('email')
		new_password1 = request.POST.get('new_password1')
		new_password2 = request.POST.get('new_password2')
		if new_password1 != new_password2:
					messages.error(request,"confirm password doesn't matched with the password")
					return redirect ('/sign')
					
		if len(new_password1)>=6 and re.search(r"[A-Z][a-z]+[@_!#$%^&*()?/}{~:]+[0-9]",new_password1):
			user = User.objects.get(email=email)
			user.set_password(new_password1)
			user.save()
			messages.info(request,"Password has been changed successfully!!")
			logout(request)
			return redirect ("/login")
			
		else:
			messages.error(request,"password should be at least 6 character long. contain both uppercase and lowercase character, at least one alpha numeric and one special charecter  (eg:Test@123)")
			return redirect("/reset_password_success")
	return render(request,'resetPassword.html')	

def staffinfo(request):
	user = User.objects.filter(is_staff=True).all()
	return render(request,'staffdata.html',{'users':user})
