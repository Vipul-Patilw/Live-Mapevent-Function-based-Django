from django.shortcuts import redirect, render
from geopy.geocoders import Nominatim
from mapeventApp.models import AddEvent
from django.contrib import messages
def addevent(request):
	if request.method =="POST":
		try:
				event = request.POST.get('event')
				info = request.POST.get('info')
				eventaddress = request.POST.get('eventaddress')
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				fromtime = request.POST.get('fromtime')
				totime = request.POST.get('totime')
				icon = request.POST.get('icon')
				eventermail = request.POST.get('eventermail')
				city = request.POST.get('city')
				geolocator = Nominatim(user_agent="MyApp")
				location = geolocator.geocode(city)
				lang = location.longitude
				lat = location.latitude
				event_poster = request.FILES.get('event_poster')
				maping = AddEvent(event=event,info=info,lang=lang,lat=lat,eventaddress=eventaddress,fromdate=fromdate,fromtime=fromtime,todate=todate,totime=totime,icon=icon, location=location,eventermail=eventermail,city=city,event_poster=event_poster)
				maping.save()
				return  redirect('/map')
		except:
			messages.error(request,"Excat location of event which you enter is invalid. please check if it don't have any spelling mistakes if it is still not working try with some official locations")
			return redirect('/addevent')
	return render (request, 'addevent.html')