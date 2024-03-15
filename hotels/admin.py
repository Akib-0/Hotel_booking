from django.contrib import admin
from . import models
# Register your models here.


class HotelAdmin(admin.ModelAdmin): # admin panel customize korte modeladmin use kori
     list_display = ['name', 'address','country' ,'created_date', 'modified_date',]
     
     prepopulated_fields = {'slug' : ('name',)}
     
admin.site.register(models.Hotel,HotelAdmin)
admin.site.register(models.Room)
admin.site.register(models.Review)
