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


# clientapp connection
from texeclientapp.views import *
from texeclientapp.models import *

# work app connection 
from texeworkapp.views import *
from texeworkapp.models import *

def login(request):
    if request.method == "POST":
        username  = request.POST.get('use')
        password = request.POST.get('pass')
        print(username)
        user = authenticate(username=username, password=password)
        try:
            if users.objects.filter(email=username, password=password,role="staff").exists():

                    member = users.objects.get(email=username, password=password)
                    request.session['userid'] = member.id
                    return redirect('staff_index')
            elif user.is_superuser:
                request.session['userid'] = request.user.id
                return redirect('dashboard')
            
            else:
            
                messages.error(request, 'Invalid username or password')
        except:
            messages.error(request, 'Invalid username or password')
    return render(request, 'home/login.html')

def dashboard(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    user=None
    data = item.objects.all()
    sub_cat=sub_category.objects.all()
    today = datetime.now()
    sub=orders.objects.filter(date__month=today.month).values_list('date__day', flat=True).distinct()
    event=events.objects.filter(start=date.today())

    nm=[]
    cnt=[]
    for i in sub:
        
        nm.append(i)
        qty=orders.objects.filter(date__day=i).count()
        cnt.append(qty)

    
 
    return render(request,'home/index.html',{'segment':segment,"user":user,'sub_cat':sub_cat,'nm':nm,
        'cnt':cnt,'data': data,'event':event})


def filter_date_event(request):
    if request.method=="POST":
        dates=request.POST.get('date_filter',None)
        segment="dashboard"
        user=None
        data = item.objects.all()
        sub_cat=sub_category.objects.all()
        today = datetime.now()
        sub=orders.objects.filter(date__month=today.month).values_list('date__day', flat=True).distinct()
        event=events.objects.filter(start=dates)

        nm=[]
        cnt=[]
        for i in sub:
            
            nm.append(i)
            qty=orders.objects.filter(date__day=i).count()
            cnt.append(qty)

        
    
        return render(request,'home/index.html',{'segment':segment,"user":user,'sub_cat':sub_cat,'nm':nm,
            'cnt':cnt,'data': data,'event':event})
    return redirect('dashboard')

def create_event(request):
    if request.method=="POST":
        st_dt=request.POST.get('start_dt',None)
        end_dt=request.POST.get('end_dt',None)
        text=request.POST.get('event_des',None)
        ev=events()
        ev.name=request.POST.get('event_des',None)
        ev.start=request.POST.get('start_dt',None)
        ev.end=request.POST.get('end_dt',None)
        ev.save()
        return redirect('dashboard')
        
    return redirect('dashboard')

def registrations(request):

    user=complaint_service.objects.all().count()
    reg=registration.objects.all().count()
    orde=orders.objects.get(id=24)

    texeclietapp_response = regist(request)
    workss = worksssddd(request)

    
    return render(request,'accounts/register.html')

def staff_home(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    staffs=users.objects.filter(role="staff")
    user=None
    return render(request,'home/staff_home.html',{'segment':segment,'staffs':staffs,'user':user,})

def add_staff(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    user=None
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
            if request.FILES.get('propic', None) == None:
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
            usr.complaint=request.POST.get('complaintss',None)
            usr.orders=request.POST.get('order',None)
            usr.preformance="0"
            usr.save()
            current_site = get_current_site(request)
            mail_subject = "Texe Registration Success"
            message = f"Hai {usr.name},\n\nUser name : {em}\nPassword : {otp}\nClick the link {current_site} to log in to your account."

            to_email = usr.email
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()
        return redirect('staff_home')


    return render(request,'home/add_staff.html',{'segment':segment,'user':user,})


def edit_staff(request,id):

    usr=users.objects.get(id=id)
    user=None
    return render(request,'home\edits_staff.html',{'usr':usr,'user':user,})
 

def save_edit_staff(request,id):
    usr=users.objects.get(id=id)

    if request.method=="POST":
        
        em=request.POST.get('email', None)
    
        
        usr.name=request.POST.get('name', None)
        usr.addres=request.POST.get('address', None)
        usr.number=request.POST.get('phn_no', None)
        if request.FILES.get('propic', None) == None:
            pass
        else:

            usr.profile=request.FILES.get('propic', None)
        usr.email=request.POST.get('email', None)
        usr.location=request.POST.get('location', None)
        usr.designation=request.POST.get('desi', None)
        usr.dob=request.POST.get('dob', None)

        usr.complaint=request.POST.get('complaintss',None)
        usr.orders=request.POST.get('order',None)
    
        usr.save()
        
        return redirect('staff_home')


    return redirect('staff_home')
def delete_staff(request,id):
    usr=users.objects.get(id=id)
    usr.delete()
    return redirect('staff_home')

def ser_cmp(request):
    comp=complaint_service.objects.filter(type="complaint")
 
    serv=complaint_service.objects.filter(type="service")
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    user=None
    context={
        'comp':comp,
        'serv':serv,
        'segment':segment,
        'user':user,
    }
    return render(request,'home/service_compl.html',context)

def add_complaint(request):
    names=users.objects.filter(role="user")
    user=None
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
        'segment':segment,
        'user':user,
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
    user=None
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
       
    return render(request,"home/add_user_complaint.html",{'segment':segment,'user':user,})


def add_service(request):
    names=users.objects.filter(role="user")
    dt= date.today()
    cmp_reg=complaint_service.objects.all().last()
    user=None
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
        'segment':segment,
        'user':user,
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
    user=None
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
       
    return render(request,"home/add_user_service.html",{'segment':segment,'user':user})

def users_lst(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    user=None
    context={
        'segment':segment,
        'user':user,
    }
    return render(request,"home/user_list.html")

def icons(request):
    return render(request,"home/icons.html")

def get_date_event(request):
    day = request.GET.get('day')
    month = request.GET.get('month')
    year = request.GET.get('year')
    all_event = events.objects.filter(start__day=day, start__month=month, start__year=year)
    names = [obj.name for obj in all_event]
    strt = [obj.start.hour for obj in all_event]
    ends = [obj.end.hour for obj in all_event]
   
    return JsonResponse({"status":" not","strt": strt,"ends":ends,"names":names})

def all_events(request):
    all_events = events.objects.all()
    out=[]
    for event in all_events:
        out.append({
            "title":event.name,
            "id":event.id,
            "start":event.start.strftime("%m/%d/%Y, %H:%M:%S"), 
        })
    return JsonResponse(out, safe=False) 
 
 
def add_event(request):
    
    if request.method == 'POST':
        start = request.POST.get('str_dt', None)
        end = request.POST.get('end_dt', None)
        title = request.POST.get('des', None)
       

        event = events(name=title, start=start,end=end, user=None) 
        event.save()
        data = {}
        return redirect('admin_home')
    return redirect('admin_home')
 
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    try:
        event = events.objects.get(id=id)
        spl=str(event.name).split(" ")
        dt=spl[0]
        or_nm=spl[1]
        date=event.start
        data = {'dt':dt,'date':date,'or_nm':or_nm}
    except:
        event = events.objects.get(id=id)
        title=event.name
        
        data = {'title':title,}
    return JsonResponse(data)

def orders_dta(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    user=None
    context={
            'segment':segment,
            'user':user,
        }
    return render(request, 'home/orders.html', context)
def prouct_list(request):
    segment="orders_dta"
    user=None
    

    items=item.objects.all()
    return render(request, 'home/product_list.html', {'items':items,'segment':segment,'user':user,})

def view_items_orders(request,id):
    segment="orders_dta"
    user=None
    names=users.objects.filter(role="user")
    user=None
    dt= date.today()
    cmp_reg=orders.objects.all().last()
    if cmp_reg:
        regst=int(cmp_reg.id)+1
    else:
        regst=1
    regss="ORD"+str(regst)+str(dt.day)+str(dt.year)[-2:]

    items=item.objects.get(id=id)
    sub=sub_images.objects.filter(item=items)
    color=sub_color.objects.filter(item=id)
    size=sub_size.objects.filter(item=id)
    
    
    context={
            'segment':segment,
            'user':user,
    
            'items':items,
            'sub':sub,
            'color':color,
            'size':size,
            'names':names,
            'regss':regss,
            'ids':id

        }
    return render(request, 'home/view_items_orders.html', context)


def add_user_order(request,id):
    user_reg=users.objects.all().last()

    segment="orders_dta"
    user=None
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
        return redirect('view_items_orders',id)
    return render(request, 'home/add_user_order.html', {'segment':segment,'user':user})


def cart_cust_size(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    itm=item.objects.get(id=prd_id)
    print(cart_id)
    ids=request.GET.get('usrs')
    usr=users.objects.get(id=ids)
    if cart_id=="":
        crt=cart_crm()
        crt.user = usr
        crt.item_id = itm.id
        crt.model = None
    else:
        crt=cart_crm.objects.get(id=cart_id)

    
    crt.size= ele
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})

def cart_change_color(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    idsr=request.GET.get('id')
    itm=item.objects.get(id=prd_id)
    ids=request.GET.get('usrs')
    usr=users.objects.get(id=ids)
    if cart_id=="":
        crt=cart_crm()
        crt.user = usr
        crt.item_id = itm.id
        crt.model = None
    else:
        crt=cart_crm.objects.get(id=cart_id) 

    
    crt.color= ele
    print(idsr)
    idata=sub_color.objects.get(id=idsr)
    crt.sub_color_id=idata.id
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})

def cart_change_meterial(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
  
    itm=item.objects.get(id=prd_id)
    ids=request.GET.get('usrs')
    usr=users.objects.get(id=ids)
    if cart_id=="":
        crt=cart_crm()
        crt.user = usr
        crt.item_id = itm.id
        crt.model = None
    else:
        crt=cart_crm.objects.get(id=cart_id) 

    
    crt.meterial= ele
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})


def cart_change_model(request):
    ele = request.GET.get('ele')
    
    model=sub_images.objects.get(id=ele)
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    itm=item.objects.get(id=prd_id)
    ids=request.GET.get('usrs')
    usr=users.objects.get(id=ids)
    if cart_id=="":
        crt=cart_crm()
        crt.user = usr
        crt.item_id = itm.id
        crt.model_id = model.id
    else:
        crt=cart_crm.objects.get(id=cart_id) 

    
    crt.model_id = model.id
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})
############################################################STAFF MODULE

def staff_index(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    ids=request.session['userid']
    user=users.objects.get(id=ids)
    print(user.role)
    context={
        'segment':segment,
        'user':user,
    }
    return render(request,"staff\staff_index.html",context)

def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')
