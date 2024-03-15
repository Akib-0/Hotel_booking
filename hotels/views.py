from django.shortcuts import render, get_object_or_404,redirect
from area.models import Area
from .models import Hotel,Room,Review
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
# Create your views here.

def hotel(request, area_slug=None):
    if area_slug : 
        area = get_object_or_404(Area, slug = area_slug)
        hotels = Hotel.objects.filter(area=area) # category wise products
        page = request.GET.get('page')
        paginator = Paginator(hotels, 2) # Paginator(objects, per page e kotogula product dekhte chai)
        paged_hotel = paginator.get_page(page)
    else : 
        hotels = Hotel.objects.all() # all hotels
        paginator = Paginator(hotels, 2) # Paginator(objects, per page e kotogula hotel dekhte chai)
        page = request.GET.get('page')
        paged_hotel = paginator.get_page(page)
        print(paged_hotel.has_next(), paged_hotel.has_previous(), paged_hotel.previous_page_number, paged_hotel.next_page_number)
        
    areas = Area.objects.all()
    context = {'hotels' : paged_hotel, 'areas' : areas, }
    return render(request, 'hotel/hotels.html', context)

# def hotel_detail(request,area_slug, hotel_slug):
#     hotel = Hotel.objects.get(slug = hotel_slug, area__slug=area_slug)
#     context = {
#         'hotel': hotel,
#     }
#     return render(request, 'hotel/hotel-detail.html', context)
# final
# def hotel_detail(request, area_slug, hotel_slug):
#     hotel = Hotel.objects.get(slug=hotel_slug, area__slug=area_slug)
#     reviews = Review.objects.filter(hotel=hotel)

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.hotel = hotel
#             review.user = request.user
#             review.save()
#             return redirect('hotel_detail', area_slug=area_slug, hotel_slug=hotel_slug)
#     else:
#         form = ReviewForm()

#     context = {
#         'hotel': hotel,
#         'reviews': reviews,
#         'form': form,
#     }
#     return render(request, 'hotel/hotel-detail.html', context)


# def hotel_detail(request, area_slug, hotel_slug):
#     hotel = get_object_or_404(Hotel, slug=hotel_slug, area__slug=area_slug)
#     user_review = Review.objects.filter(hotel=hotel, user=request.user).first()
#     reviews = Review.objects.filter(hotel=hotel)

#     if request.method == 'POST':
#         if user_review:
#             form = ReviewForm(request.POST, instance=user_review)
#         else:
#             form = ReviewForm(request.POST)
            
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.hotel = hotel
#             review.user = request.user
#             review.save()
#             return redirect('hotel_detail', area_slug=area_slug, hotel_slug=hotel_slug)
#     else:
#         form = ReviewForm(instance=user_review)

#     context = {
#         'hotel': hotel,
#         'reviews': reviews,
#         'form': form,
#     }
#     return render(request, 'hotel/hotel-detail.html', context)


def hotel_detail(request, area_slug, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug, area__slug=area_slug)
    user_review = None
    reviews = Review.objects.filter(hotel=hotel)

    if request.user.is_authenticated:
        user_review = Review.objects.filter(hotel=hotel, user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        if user_review:
            form = ReviewForm(request.POST, instance=user_review)
        else:
            form = ReviewForm(request.POST)
            
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = hotel
            review.user = request.user
            review.save()
            return redirect('hotel_detail', area_slug=area_slug, hotel_slug=hotel_slug)
    else:
        form = ReviewForm(instance=user_review)

    context = {
        'hotel': hotel,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'hotel/hotel-detail.html', context)

def search_hotel(request):
    hotels = []
    h_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            hotels = Hotel.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | 
                Q(name__icontains=keyword) | 
                Q(area__area_name__icontains=keyword) | 
                Q(room__room_type__icontains=keyword) 
            )
            print(keyword)
            h_count = hotels.count()

    context = {
        'hotels': hotels,
        'h_count': h_count,
    }
    return render(request, 'hotel/hotels.html', context)
       
# @login_required
# def leave_review(request):
#     hotel = get_object_or_404(Hotel)
#     if request.method == 'POST':
#         rating = int(request.POST.get('rating'))  # Assuming the rating is provided as an integer
#         comment = request.POST.get('comment')
#         review = Review.objects.create(
#             user=request.user,
#             hotel=hotel,
#             rating=rating,
#             comment=comment,
#             created_at=timezone.now()
#         )
#         return redirect('hotel_detail')
#     return render(request, 'hotel/hotel-detail.html', {'hotel': hotel})

# def submit_review(request,hotel_id):
#     url = request.Meta.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             reviews = Review.objects.get(user__id=request.user.id,hotel__id=hotel_id)
#             form = ReviewForm(request.POST,instance=reviews)
#             form.save()
#             #messages.success(request,'Thank you!Your review has been updated')
#             return redirect(url)
#         except Review.DoesNotExist:
#             form = ReviewForm(request.POST)
#             data = Review()
#             data.subject = form.cleaned_data['subjects']
#             data.rating = form.cleaned_data['rating']
#             data.review = form.cleaned_data['review']
#             data.ip = request.Meta.get('REMOTE_ADDR')
#             data.hotel_id = hotel_id
#             data.save()
#             return redirect(url)

def submit_review(request, hotel_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.hotel_id = hotel_id
            data.user = request.user
            data.save()
            return redirect(url)
    return redirect('hotel_detail')