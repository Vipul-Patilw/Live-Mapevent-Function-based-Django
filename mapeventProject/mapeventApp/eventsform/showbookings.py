from mapeventApp.models import Event,Login
from django.shortcuts import redirect, render
def booking_admin_view(request):
	if request.method =="POST":
		email = request.POST.get('email')
		event = request.POST.get('event')
		events1 = Event.objects.filter(event=event).all()
		events = Event.objects.filter(email=email).all()
		return render (request,'booking2.html', {'events':events,'events1':events1})
	eventscount = Event.objects.all()
	events2 = Event.objects.all().values_list('event', flat=True).distinct()
#	events2 = Event.objects.values('event' ).annotate(Count('id')).order_by().filter(id__count__gt=1)
	try:
		events3 = Event.objects.filter(event=events2[0]).count()
		
	except:
		return render(request,'booking.html')

	
	main = {'events1':events2,'events3':events3,'eventcount':eventscount}
	
	return render (request,'booking.html',main)

def booking_user_view(request, email):
		events = Event.objects.filter(email=email).all()
		
		
		return render (request,'booking.html', {'events':events,})
	