from django.shortcuts import redirect, render
from geopy.geocoders import Nominatim
from mapeventApp.models import AddEvent
from django.contrib import messages
from django.core import paginator
def updateEventpage(request):

	page = int(request.GET.get('page', 1))
	allevents = AddEvent.objects.all()
	p = paginator.Paginator(allevents,9)
	try:
		event_page = p.page(page)
	except paginator.EmptyPage:
				event_page = paginator.Page([], page, p)	
	return render(request,'editevent.html',{'event_page':event_page})
	

def updateEvent(request,event_id):
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
				maping = AddEvent.objects.get(id=event_id)
				maping.event=event
				if request.FILES.get('event_poster'):
					event_poster = request.FILES.get('event_poster')
					maping.event_poster = event_poster
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
				maping.save()
				messages.success(request,"event has been updated successfully")
				return redirect('/eventeditpage')
			except Exception as e:
				messages.error(request,f"error :{e}, Excat location of event which you enter is invalid. please check if it don't have any spelling mistakes if it is still not working try with some official locations")
				context = {
                'updates': AddEvent.objects.filter(id=event_id).all(),
                'form_data': request.POST,  # Pass the form data back to the template
				}
				return render(request, 'updateEvent.html', context)
		updates = AddEvent.objects.filter(id=event_id).all()
		return render(request,'updateEvent.html',{'updates': updates})
		