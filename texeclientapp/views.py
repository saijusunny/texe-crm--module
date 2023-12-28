from django.shortcuts import render
from .models import *


def regist(request):

	dt=registration.objects.get(id="6")
	print("second")
	print(dt)
	return render(request, 'accounts/register.html')