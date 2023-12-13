from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *

from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
import random
import string

from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

# from requests import request

def login(request):
    # views.py or other files in your current app
    print("dsfs")
    return render(request, 'home/login.html')

def dashboard(request):
    return render(request,'home/index.html')
def registration(request):
    return render(request,'home/register.html')
def users(request):
    return render(request,"home/user_list.html")