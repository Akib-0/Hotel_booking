from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotels')
    return render(request, 'accounts/register.html', {'form':form})

def profile(request):
    return render(request, 'accounts/dashboard.html')

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(username = user_name, password = password)
        if user is not None:
            login(request, user)
            return redirect('hotels')
        else:
           return render(request, 'accounts/signin.html') 
    return render(request, 'accounts/signin.html')

def user_logout(request):
    logout(request)
    return redirect('login')