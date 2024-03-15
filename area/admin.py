from django.contrib import admin
from .models import Area
# Register your models here.

# admin.site.register(Category)

class AreaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('area_name',)}
    list_display = ('area_name', 'slug')
    
admin.site.register(Area, AreaAdmin)