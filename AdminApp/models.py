from django.db import models

# Create your models here.
class Category(models.Model):
    cname=models.CharField(max_length=20)

    class Meta:
        db_table="Category"
    def __str__(self):
        return f"Category: {self.cname}"

class Cake(models.Model):
    cake_name=models.CharField(max_length=20)
    price=models.IntegerField(null=True)
    image=models.ImageField(default="abc.jpg",upload_to="Images")
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta():
        db_table="Cake"
    def __str__(self):
        return f"Cake: {self.cake_name}"