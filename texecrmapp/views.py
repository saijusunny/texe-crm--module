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
from django.urls import resolve
# from requests import request

def login(request):
    if request.method == "POST":
        username  = request.POST.get('use')
        password = request.POST.get('pass')
        print(username)
        user = authenticate(username=username, password=password)
        if user.is_superuser:
            request.session['userid'] = request.user.id
            return redirect('dashboard')
        else:
            pass
    return render(request, 'home/login.html')

def dashboard(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    return render(request,'home/index.html',{'segment':segment})

def registration(request):
    return render(request,'accounts/register.html')

def staff_home(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    return render(request,'home/staff_home.html',{'segment':segment})

def add_staff(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    if request.method=="POST":
        user_reg=users.objects.all().last()
        dt= date.today()
        digits = string.digits
        otp = ''.join(random.choices(digits, k=6))
        if user_reg:
            regst=int(user_reg.id)+1
        else:
            regst=1
        usr=users()
        em=request.POST.get('email', None)
        if users.objects.filter(email=em).exists():
           
            messages.error(request,"Email Already exists !")
            return redirect('add_staff')
        else:
            usr.regno= "STF"+str(regst)+str(dt.day)+str(dt.year)[-2:]
            usr.name=request.POST.get('name', None)
            usr.addres=request.POST.get('address', None)
            usr.number=request.POST.get('phn_no', None)
            if request.FILES.get('propic', None) == "":
                usr.profile= 'static\images\static_image\icon.svg'
            else:

                usr.profile=request.FILES.get('propic', None)
            usr.email=request.POST.get('email', None)
            usr.location=request.POST.get('location', None)
            usr.designation=request.POST.get('desi', None)
            usr.dob=request.POST.get('dob', None)
            usr.status="active"
            usr.role="staff"
            usr.password=otp
            usr.save()
            current_site = get_current_site(request)
            mail_subject = "Texe Registration Success"
            message = f"Hai {usr.name},\n\nUser name : {em}\nPassword : {otp}\nClick the link {current_site} to log in to your account."

            to_email = usr.email
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()
        return redirect('staff_home')


    return render(request,'home/add_staff.html',{'segment':segment})

def ser_cmp(request):
    comp=complaint_service.objects.filter(type="complaint")
 
    serv=complaint_service.objects.filter(type="service")
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    context={
        'comp':comp,
        'serv':serv,
        'segment':segment
    }
    return render(request,'home/service_compl.html',context)

def add_complaint(request):
    names=users.objects.filter(role="user")
    dt= date.today()
    cmp_reg=complaint_service.objects.all().last()
    if cmp_reg:
        regst=int(cmp_reg.id)+1
    else:
        regst=1
    regss="CMP"+str(regst)+str(dt.day)+str(dt.year)[-2:]
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    context={
        "names":names,
        "regss":regss,
        'segment':segment
    }
    
    if request.method=="POST":
        
        com_srv=complaint_service()
        usr=request.POST.get('name')
        usrid=users.objects.get(id=usr)
        com_srv.users=usrid
        com_srv.regno=request.POST.get('regno')
        com_srv.complaint=request.POST.get('complaint')
        com_srv.type="complaint"
        com_srv.status="pending"
        com_srv.save()
        current_site = get_current_site(request)
        mail_subject = "Texe Complaint Registred"
        message = f"Hai {usrid.name},\n\nUser name : {usrid.email}\nPassword : {usrid.password}\nClick the link {current_site} to view your given complaint status"

        to_email = usrid.email
        send_email = EmailMessage(mail_subject,message,to = [to_email])
        send_email.send()

        return redirect('ser_cmp')
    
    return render(request,"home/add_complaint.html",context)

def add_user_complaint(request):
    user_reg=users.objects.all().last()
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    if request.method=='POST':
        urs=users()
        dt= date.today()
        digits = string.digits
        otp = ''.join(random.choices(digits, k=6))
        if user_reg:
            regst=int(user_reg.id)+1
        else:
            regst=1
        urs.regno= "CUS"+str(regst)+str(dt.day)+str(dt.year)[-2:]
        urs.name = request.POST.get('name',None)
        urs.email = request.POST.get('email',None)
        urs.number = request.POST.get('phn_no',None)
        urs.password = otp
        if request.FILES.get('propic',None)=="":
            pass
        else:
            profile = request.FILES.get('propic',None)
        urs.joindate = date.today()
        urs.status ="active"
        urs.addres =  request.POST.get('address',None)
        urs.role = "user"
        urs.save()
        return redirect('add_complaint')
       
    return render(request,"home/add_user_complaint.html",{'segment':segment})


def add_service(request):
    names=users.objects.filter(role="user")
    dt= date.today()
    cmp_reg=complaint_service.objects.all().last()
    if cmp_reg:
        regst=int(cmp_reg.id)+1
    else:
        regst=1
    regss="SER"+str(regst)+str(dt.day)+str(dt.year)[-2:]
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    context={
        "names":names,
        "regss":regss,
        'segment':segment
    }
    
    if request.method=="POST":
        
        com_srv=complaint_service()
        usr=request.POST.get('name')
        usrid=users.objects.get(id=usr)
        com_srv.users=usrid
        com_srv.regno=request.POST.get('regno')
        com_srv.complaint=request.POST.get('complaint')
        com_srv.type="service"
        com_srv.status="pending"
        com_srv.save()
        current_site = get_current_site(request)
        mail_subject = "Texe Complaint Registred"
        message = f"Hai {usrid.name},\n\nUser name : {usrid.email}\nPassword : {usrid.password}\nClick the link {current_site} to view your given service status"

        to_email = usrid.email
        send_email = EmailMessage(mail_subject,message,to = [to_email])
        send_email.send()

        return redirect('ser_cmp')
    
    return render(request,"home/add_service.html",context)

def add_user_service(request):
    user_reg=users.objects.all().last()
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    if request.method=='POST':
        urs=users()
        dt= date.today()
        digits = string.digits
        otp = ''.join(random.choices(digits, k=6))
        if user_reg:
            regst=int(user_reg.id)+1
        else:
            regst=1
        urs.regno= "CUS"+str(regst)+str(dt.day)+str(dt.year)[-2:]
        urs.name = request.POST.get('name',None)
        urs.email = request.POST.get('email',None)
        urs.number = request.POST.get('phn_no',None)
        urs.password = otp
        if request.FILES.get('propic',None)=="":
            pass
        else:
            profile = request.FILES.get('propic',None)
        urs.joindate = date.today()
        urs.status ="active"
        urs.addres =  request.POST.get('address',None)
        urs.role = "user"
        urs.save()
        return redirect('add_service')
       
    return render(request,"home/add_user_service.html",{'segment':segment})

def users_lst(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    context={
        'segment':segment
    }
    return render(request,"home/user_list.html")

def icons(request):
    return render(request,"home/icons.html")