from django.contrib import admin
from AdminApp.models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=("id","cname")
class CakeAdmin(admin.ModelAdmin):
    list_display=("id","cake_name","price","image","category")

admin.site.register(Category,CategoryAdmin)
admin.site.register(Cake,CakeAdmin)