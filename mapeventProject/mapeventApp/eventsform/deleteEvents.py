from mapeventApp.models import AddEvent,Add
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
def deleteEvent(request):
	if request.method =="POST":
			event = request.POST.get('event')
			box = request.POST.get('box')
			add1 = Add(event=event,box=box)
			add1.save()
			add = AddEvent.objects.all()
			if box == "on":
				events = AddEvent.objects.get(event=event)
				events.delete()
				messages.success(request,"Events Deleted succesfully")
			return redirect('/deleteEvent',{'adds':add})
	add = AddEvent.objects.all()
	return render(request,'deleteevent.html',{'adds':add})

