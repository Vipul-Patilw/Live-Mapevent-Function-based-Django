#pylint:disable=E0001
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views,home,context_processors

from mapeventApp.eventsform import addevent,showbookings,staffrequest,updateEvents,deleteEvents,bookevents
from .views import changePassword
urlpatterns = [
   path('sign',views.index, name='sign'),
   path('logininfo',views.index, name='sign'),#path('map',home.base),
   
   path('importexportevent', views.import_export_event_csv,name="importexport event"),  
        path('qr_generator',views.qr_code_generator,name="qr_generator") ,   
  #  path('importexportevent',views.Import_csv, name='importexportvent'),
   path('login',views.sign, name='login'),
   path('map',home.map, name='map'),
   path('searchdetail',views.searchDetail, name='searchdetail'),
   path('eventeditpage',updateEvents.updateEventpage, name='alleventedit'),
   path('editevents',updateEvents.updateEvent, name='editevents'),
   path('locate-<lat>&<lang>',home.locate, name='locate'),
   path('eventdetails-<event_id>',home.eventdetail, name='eventdetails'),
   path('',home.map, name='map'),
   path('pass',changePassword.as_view(template_name='changePassword.html')),
 #  path('set',changePassword.as_view(template_name='resatePassword.html')),
   path('password_success',views.password_success, name='password_success'),
 #  path('map',home.autocompleteModel, name='home'),
   path('personaldetails',views.personalDetails, name='personaldetails'),
   path('eventform',bookevents.events, name='eventform'),
  path('adminlogin',views.adminlogin, name='admin'),
  path('adminsignIn',views.adminsign, name='adminsign'),
  path('bookingform-<event_id>-<email>',home.booking, name='booking_form'),
  path('booking',showbookings.booking_admin_view, name='booking_users'),
  path('booking-<email>',showbookings.booking_user_view, name='bookinguser'),
  path('request',staffrequest.request, name='request'),
  path('staffdata',views.staffinfo, name='staffdata'),
  path('deleteEvent',deleteEvents.deleteEvent, name='delteEvent'),
   path('logout',views.logoutuser, name='logout'),
   path('forgotPassword',views.forgotpassword, name='forgotpassword'),
   path('reset_password_success',views.reset_password_success, name='reset_password_success'),
   path('reset_password_success/<uidb64>/<token>',views.resetpasswordlink, name='reset_password_success'),
   path('addevent',addevent.addevent, name='eventadd'),
   path('gotologin',views.gotologin, name='gotologin'),
   path('activate/<uidb64>/<token>',views.activate, name='activate'),

]

