from django.shortcuts import render

from .models import *

def worksssddd(request):
	print("third")
	obs=complaint_service.objects.all().count()
	print(obs)
	return render(request, "home/login.html")