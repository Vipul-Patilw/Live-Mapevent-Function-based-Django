from mapeventApp.models import AddEvent,Staff
from geopy.geocoders import Nominatim
from django.shortcuts import redirect,render
from django.core import  paginator
import datetime
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def base(request):
	if 'basecity' in request.POST:
		basecity = request.POST.get('basecity')
		citynameunique = AddEvent.objects.filter(city=basecity).all().values_list('city', flat=True).distinct()
		evntsbasecount = AddEvent.objects.filter(city=basecity)

		geolocators = Nominatim(user_agent="MyApp")
		baselocation = geolocators.geocode(basecity)
		baselang = baselocation.longitude
		baselat = baselocation.latitude
		page2 = int(request.GET.get('page', 1))
		p2 = paginator.Paginator(evntsbasecount,8)
		try:
			event_page2 = p2.page(page2)
		except paginator.EmptyPage:
			event_page2 = paginator.Page([], page2, p2)
		if  not is_ajax(request):
		          context = {
            'eventbasepaging': event_page2,
            'eventbasecount':evntsbasecount,
            'citynameunique':citynameunique, 
            'baselat':baselat,
	'baselang':baselang,
        }
        		  return context
        		  	
		else:
			content2 = ''
			for event in event_page2:
				content2 += render_to_string('list-events.html',{'page': event},request=request)
				return JsonResponse({
            "content": content2,
            "end_pagination": True if page2 >= p2.num_pages else False,
        })
	dd = "dd"
	return {'dd':dd}
#	else:
#		evntsbasecount = ""
#		citynameunique= ""
#		baselat=""
#		baselang=""
		

def locations(request):
	date=datetime.date.today()
	staff = Staff.objects.all()
	
	#if 'basecity' in request.POST:
#		basecity = request.POST.get('basecity')
#		citynameunique = AddEvent.objects.filter(city=basecity).all().values_list('city', flat=True).distinct()
#		evntsbasecount = AddEvent.objects.filter(city=basecity)

#		geolocators = Nominatim(user_agent="MyApp")
#		baselocation = geolocators.geocode(basecity)
#		baselang = baselocation.longitude
#		baselat = baselocation.latitude
#		page = int(request.GET.get('page', 1))
#		p = paginator.Paginator(evntsbasecount,8)
#		try:
#			event_page = p.page(page)
#		except paginator.EmptyPage:
#			event_page = paginator.Page([], page, p)
#		if  not is_ajax(request):
#		          context = {
#            'eventbasepaging': event_page,'evntsbasecount										':evntsbasecount
#        }
#        		  return render(request,
#                      'map.html',
#                      context)
#	
#		else:
#			content = ''
#			for event in event_page:
#				content += render_to_string('list-events.html',{'page': event},request=request)
#				return JsonResponse({
#            "content": content,
#            "end_pagination": True if page >= p.num_pages else False,
#        })
		#context_redirect ={}
#		redirects = redirect('/map')
#		context_redirect.update(redirects)
	#	return render(request,'map.html',{'baselat':baselat,'baselang':baselang}
	
	
	locations = AddEvent.objects.all().values_list('city', flat=True).distinct() 
	
	dict = {
	'locations':locations,
'date':date,
'staff':staff
}
	return dict

			