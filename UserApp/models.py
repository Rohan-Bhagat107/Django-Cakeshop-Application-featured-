from django.db import models
from AdminApp.models import Cake, Category
from datetime import datetime
from datetime import timedelta
# Create your models here.
current_date=datetime.now()
class UserInfo(models.Model):
    username=models.CharField(max_length=20,primary_key=True)
    email=models.EmailField(max_length=25,null=True)
    password=models.CharField(max_length=25)
    class Meta():
        db_table="UserInfo"
    def __str__(self):
        return self.username

class MyCart(models.Model):
    cake=models.ForeignKey(Cake,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(UserInfo,on_delete=models.SET_NULL,null=True)
    qty=models.IntegerField(default=2)
    class Meta():
        db_table="MyCart"
# class OrderHistory(models.Model):
 
#     order_date=models.DateTimeField(auto_now=True)
#     order_item=models.ForeignKey(MyCart,on_delete=models.SET_NULL,null=True)
#     user=models.ForeignKey(UserInfo,on_delete=models.SET_NULL,null=True)
#     amount=models.IntegerField()
#     card_no=models.IntegerField(null=True)
#     delivery_date=models.DateTimeField(default=current_date+ timedelta(days=5))
    
#     class Meta():
#         db_table="Order History"
class OrderHistory(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    cake_name = models.CharField(max_length=100,null=True,blank=True)
    cake_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    card_no = models.CharField(max_length=16)

    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(default=current_date+ timedelta(days=5))
    class Meta():
        db_table="Order History"

    def __str__(self):
        return f"Order {self.id} - {self.cake_name}"


class CardDetails(models.Model):
    card_no=models.IntegerField(max_length=12)
    cvv=models.IntegerField(max_length=3,null=True)
    expiry_date=models.CharField(max_length=7,null=True)
    user=models.ForeignKey(UserInfo,on_delete=models.CASCADE,null=True)

    class Meta():
        db_table="Card Details"