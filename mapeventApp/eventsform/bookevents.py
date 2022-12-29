#!/usr/bin/python
# -*- coding: utf-8 -*-
from mapeventApp.models import Event
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from mapeventProject import settings
from django.shortcuts import redirect, render


def events(request):
    if request.method == 'POST':
           try:
           	     event = request.POST.get('event')
           	     eventaddress = request.POST.get('eventaddress')
           	     dtime = request.POST.get('dtime')
           	     full_name = request.POST.get('full_name')
           	     email = request.POST.get('email')
           	     emailowner = request.POST.get('emailowner')
           	     mobile_number = request.POST.get('mobile_number')
           	     date = request.POST.get('date')
           	     time = request.POST.get('time')
           	     even = Event(
			            email=email,
			            emailowner=emailowner,
			            mobile_number=mobile_number,
			            full_name=full_name,
			            eventaddress=eventaddress,
			            event=event,
			            date=date,
			            time=time,
			            dtime=dtime,
			            )
           	     even.save()
           	     messages.info(request, event)
           	     current_site = get_current_site(request)
           	     emailsub = 'Event Booking Successfull'
           	     emailbody = render_to_string('mailsendtourself.html', {
			            'eventaddress': eventaddress,
			            'domain': current_site.domain,
			            'name': full_name,
			            'event': event,
			            'dtime': dtime,
			            })
           	     from_mail = settings.EMAIL_HOST_USER
           	     to_mail = [email]
           	     email = EmailMessage(emailsub, emailbody, from_mail, to_mail)
           	     email.fail_silently = True
           	     email.send()
           	     emailsub = 'User book the event'
           	     emailbody = render_to_string('mailsendtoOther.html', {
			            'domain': current_site.domain,
			            'event': event,
			            'name': full_name,
			            'mobile': mobile_number,
			            'email': even.email,
			            'datetime': date,
			            })
           	     from_mail = settings.EMAIL_HOST_USER
           	     to_mail = [emailowner]
           	     email = EmailMessage(emailsub, emailbody, from_mail, to_mail)
           	     email.fail_silently = True
           	     email.send()
           	     return redirect('/map')
           
           
           except:
           	#messages.error(request,"mail has not sent cause Google ban smtp feature from 30may 2022. you can check your bookings from here;")
           	return redirect('/map')
    return render(request, 'eventForm1.html')
			        