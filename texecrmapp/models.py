
from django.db import models
from datetime import datetime,date, timedelta

class OtherProjectModel(models.Model):
    # Your fields go here

    class Meta:
        app_label = 'texeclientapp'
        db_table = 'orders'

class users(models.Model):
    regno= models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    number = models.CharField(max_length=250, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    profile = models.ImageField(upload_to='images/propic',null=True, blank=True, default="static\images\static_image\icon.svg")
    joindate = models.DateField(null=True, default=date.today())
    last_login = models.DateTimeField(null=True, blank=True)  
    status =models.CharField(max_length = 255,blank=True,null=True, default="active")
    addres =  models.TextField(blank=True,null=True)
    role = models.CharField(max_length=255,blank=True,null=True)
    dob=models.DateField(null=True,)
    location = models.CharField(max_length=250, null=True, blank=True)
    otp= models.CharField(max_length=250, null=True, blank=True)
    designation=models.CharField(max_length=250, null=True, blank=True)
    complaint=models.CharField(max_length=250, null=True, blank=True)
    orders=models.CharField(max_length=250, null=True, blank=True)
    preformance=models.CharField(max_length=250, null=True, blank=True)
    def get_email_field_name(self):
        return 'email'

class complaint_service(models.Model):
    
    users = models.ForeignKey(users, on_delete=models.SET_NULL, null=True, blank=True)
    regno= models.CharField(max_length=255,blank=True,null=True)
    complaint = models.TextField(blank=True,null=True)
    status= models.CharField(max_length=255,blank=True,null=True)
    date_register= models.DateField(default=date.today())
    type= models.CharField(max_length=255,blank=True,null=True)


class events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True,null=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    user=models.ForeignKey(users, on_delete=models.CASCADE, null=True, blank=True)
