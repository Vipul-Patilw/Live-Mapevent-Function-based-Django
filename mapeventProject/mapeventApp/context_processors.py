from mapeventApp.models import AddEvent,Staff
from geopy.geocoders import Nominatim
from django.shortcuts import redirect,render
from django.core import  paginator
import datetime
def locations(request):
	date=datetime.date.today()
	staff = Staff.objects.all()
	
	if 'basecity' in request.POST:
		basecity = request.POST.get('basecity')
		citynameunique = AddEvent.objects.filter(city=basecity).all().values_list('city', flat=True).distinct()
		evntsbasecount = AddEvent.objects.filter(city=basecity)
		geolocators = Nominatim(user_agent="MyApp")
		baselocation = geolocators.geocode(basecity)
		baselang = baselocation.longitude
		baselat = baselocation.latitude
		#context_redirect ={}
#		redirects = redirect('/map')
#		context_redirect.update(redirects)
	#	return render(request,'map.html',{'baselat':baselat,'baselang':baselang}
	
	else:
		baselang = ""
		baselat = ""
		eventbasepaging=""
		evntsbasecount=""
		citynameunique=""		
	locations = AddEvent.objects.all().values_list('city', flat=True).distinct() 
	
	dict = {
	'locations':locations,
	'baselat':baselat,
	'baselang':baselang,'eventbasepaging':evntsbasecount,'eventbasecount':evntsbasecount,
'citynameunique':citynameunique,
'date':date,
'staff':staff
}
	return dict

			