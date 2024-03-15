from django.urls import path
from . import views
urlpatterns = [
    path('', views.hotel, name='hotels'),
    path('area/<slug:area_slug>/', views.hotel, name='hotels_by_area'),
    path('<slug:area_slug>/<slug:hotel_slug>/', views.hotel_detail, name='hotel_detail'),
    path('search/', views.search_hotel, name='search'),
]