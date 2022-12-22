from mapeventApp.models import AddEvent,Staff,Login
from django.shortcuts import redirect, render
from django.core import paginator
from django.template.loader import render_to_string
import datetime
from django.http import JsonResponse,HttpResponse
#from django.utils import simplejson
import json
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#def autocompleteModel(request):
#    search_qs = AddEvent.objects.filter(event__startswith=request.REQUEST['search'])
#    results = []
#    for r in search_qs:
#        results.append(r.name)
#    resp = request.REQUEST['callback'] + '(' + simplejson.dumps(results) + ');'
#    return HttpResponse(resp, content_type='application/json')
    
def map(request):
	date=datetime.date.today()
	page = int(request.GET.get('page', 1))
	events = AddEvent.objects.filter(todate__gte=date).all().order_by('fromdate').values()
	p = paginator.Paginator(events,8)
	if request.user.is_anonymous:
			return redirect ("/login")
	if 'search' in request.POST:
				
					search= request.POST.get('search')
					events = AddEvent.objects.filter(event__icontains = search).all()
					location = AddEvent.objects.filter(location__icontains = search).all()
					return render(request,'searchdetail.html',{'events':events,'searches':search,'locations':location})


	try:
		event_page = p.page(page)
	except paginator.EmptyPage:
		event_page = paginator.Page([], page, p)
		
	if  not is_ajax(request):
		context = {
            'events': event_page,'mapings':events
        }
		return render(request,
                      'map.html',
                      context)
	
	else:
		content = ''
		for event in event_page:
			content += render_to_string('list-events.html',{'page': event},request=request)
		return JsonResponse({
            "content": content,
            "end_pagination": True if page >= p.num_pages else False,
        })
	

	
	#if request.method =="POST":
#	if 'satelite' in request.POST:
#		style_map= request.POST.get('satelite')
#	if 'street' in request.POST:
#		style_map= request.POST.get('street')
#	if 'satelite' not in request.POST and 'street' not in request.POST:
#		style_map= "streets-v11"
	
	maping1 = {'mapings':events}#'style_map':style_map}
	
	return render (request,'map.html',maping1,)

def eventdetail(request,event_id):
			eventsinfo = AddEvent.objects.filter(id= event_id).all()
			return render(request,'eventdetail.html',{'eventinfo':eventsinfo})
			
def locate(request,lat,lang):
	date=datetime.date.today()
	page = int(request.GET.get('page', 1))
	events = AddEvent.objects.filter(todate__gte=date).all().order_by('fromdate').values()
	p = paginator.Paginator(events,10)
	try:
		event_page = p.page(page)
	except paginator.EmptyPage:
		event_page = paginator.Page([], page, p)
	return  render(request,'map.html',{'lat':lat,'lang':lang,'mapings':events,'events':event_page})

def booking(request,event_id,email):
	
				eventsbook = AddEvent.objects.filter(id= event_id).all()
				user = Login.objects.filter(email=email).all()
				return render(request,'eventForm1.html',{'bookevents':eventsbook,'users':user})

