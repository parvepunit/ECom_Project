from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import * 
# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True)
    phone_no = models.CharField(max_length=14)
    is_phone_no_verified = models.BooleanField(default=False)

    objects= UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Order(models.Model):
    STATUS = (
        ('In Process', 'In Process'),
        ('Shipped','Shipped'),
        ('Deliverd', 'Deliverd'),
    ) 

    customer = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    order_name = models.CharField(max_length=100, null=True)
    order_address = models.CharField(max_length=200, null=True)
    order_deliveryState = models.CharField(max_length=50, null=True)
    order_phone = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    order_id = models.CharField(max_length=50, null=True)
    order_details = models.CharField(max_length=300, null=True)
    order_amount = models.CharField(max_length=50, null=True)
    order_trackingId = models.CharField(max_length=50,default="Awaiting Shipping", null=True)
    order_status = models.CharField(max_length=50, choices=STATUS)
    payment_status = models.CharField(max_length=50, default="N.A.", null=True)
    pg_transact_id = models.CharField(max_length=50 ,blank=True, null=True)
    payment_instrument = models.CharField(max_length=500,blank=True, null=True)
    

    
    def __str__(self) -> str:
        return self.order_id

    
class Customer(models.Model):
    state_choice = [("Andhra Pradesh", "Andhra Pradesh"), ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),("Assam", "Assam"), ("Bihar", "Bihar"),("Chandigarh", "Chandigarh"),
    ("Chhattisgarh", "Chhattisgarh"),("Dadar and Nagar Haveli", "Dadar and Nagar Haveli"),
    ("Daman and Diu", "Daman and Diu"),("Delhi", "Delhi"), ("Lakshadweep", "Lakshadweep"),("Puducherry", "Puducherry"),
    ("Goa", "Goa"),("Gujarat", "Gujarat"), ("Haryana", "Haryana"),("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu and Kashmir", "Jammu and Kashmir"),("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"),("Kerala", "Kerala"), ("Madhya Pradesh", "Madhya Pradesh"),("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"),("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"),("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),("Telangana", "Telangana"), ("Tripura", "Tripura"),("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),("West Bengal", "West Bengal")]
    user = models.OneToOneField(CustomUser,null=True, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=300,null=True)
    address2 = models.CharField(max_length=300,null=True)
    city = models.CharField(max_length=50,null=True)
    State = models.CharField(max_length=50,null=True, choices=state_choice)
    zip = models.CharField(max_length=6,null=True)
    
    def __str__(self) -> str:
        return (self.user.first_name + self.user.last_name)