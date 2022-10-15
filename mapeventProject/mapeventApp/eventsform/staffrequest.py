from mapeventApp.models import Staff
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
def request(request):
	if request.method =="POST" and 'user' in request.POST:
			username = request.POST.get('username')
			users = User.objects.get(username=username)
			users.is_active = True
			users.is_staff = True
			users.save()
			staff = Staff.objects.get(username=username)
			staff.delete()
			messages.success(request,f"{users.first_name} {users.last_name} request for staff account accessed is accepted ")
			return redirect('/request')
	if request.method =="POST" and 'user1' in request.POST:
			username1 = request.POST.get('username1')
			users = User.objects.get(username=username1)
			staff = Staff.objects.get(username=username1)
			staff.delete()
			messages.success(request,f"{users.first_name} {users.last_name} request for staff account accessed is Rejected ")
			return redirect('/request')
	
	user = Staff.objects.all()
	return render(request,'request.html',{'users':user})