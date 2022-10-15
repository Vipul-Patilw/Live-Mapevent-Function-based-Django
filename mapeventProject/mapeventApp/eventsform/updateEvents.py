from django.shortcuts import redirect, render
from geopy.geocoders import Nominatim
from mapeventApp.models import AddEvent
from django.contrib import messages
from django.core import paginator
def updateEventpage(request):
	if request.method =="POST":
			event_id = request.POST.get('event_id')
			updates = AddEvent.objects.filter(id=event_id).all()
			return render(request,'updateEvent.html',{'updates': updates})
	page = int(request.GET.get('page', 1))
	allevents = AddEvent.objects.all()		
	p = paginator.Paginator(allevents,7)
	try:
		event_page = p.page(page)
	except paginator.EmptyPage:
				event_page = paginator.Page([], page, p)	
	return render(request,'editevent.html',{'event_page':event_page})
	

def updateEvent(request):
		if request.method =="POST":
			try:
				event_id = request.POST.get('event_id')
				event = request.POST.get('event')
				info = request.POST.get('info')
				eventaddress = request.POST.get('eventaddress')
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				fromtime = request.POST.get('fromtime')
				totime = request.POST.get('totime')
				locate = request.POST.get('locate')
				icon = request.POST.get('icon')
				eventermail = request.POST.get('eventermail')
				city = request.POST.get('city')
				geolocator = Nominatim(user_agent="MyApp")
				location = geolocator.geocode(locate)
				lang = location.longitude
				lat = location.latitude
				maping = AddEvent.objects.get(id=event_id)
				maping.info=info
				maping.lang=lang
				maping.lat=lat
				maping.eventaddress=eventaddress
				maping.fromdate=fromdate
				maping.fromtime=fromtime
				maping.todate=todate
				maping.totime=totime
				maping.icon=icon
				maping.location=location
				maping.eventermail=eventermail
				maping.city=city
				maping.locate = locate
				maping.save()
				messages.success(request,"events has been updated successfully")
				return redirect('/eventeditpage')
			except:
				messages.error(request,"Excat location of event which you enter is invalid. please check if it don't have any spelling mistakes if it is still not working try with some official locations")
				return redirect('/addevent')
		return render(request,'updateEvent.html')
		