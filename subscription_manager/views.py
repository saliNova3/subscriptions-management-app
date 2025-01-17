from django.shortcuts import render, redirect
from django.urls import reverse

def home_view(request):
    if request.user.is_authenticated:
        # If user is logged in, redirect to the subscriptions list
        return redirect(reverse('subscriptions:list'))
    else:
        # Otherwise show a landing page or login page
        return render(request, 'home.html') 
