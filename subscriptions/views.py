from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subscription
from .forms import SubscriptionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .forms import MyLoginForm
from .forms import CustomUserCreationForm

@login_required
def subscription_list(request):
    """
    List all subscriptions for the currently logged-in user.
    """
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})

@login_required
def subscription_detail(request, pk):
    """
    Show details of a single subscription, ensuring it belongs to the logged-in user.
    """
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    return render(request, 'subscriptions/subscription_detail.html', {'subscription': subscription})

@login_required
def subscription_create(request):
    """
    Handle form display and submission for creating a new subscription.
    Assign the subscription to the current user.
    """
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user  # Link to the user
            subscription.save()
            return redirect('subscriptions:list')
    else:
        form = SubscriptionForm()

    return render(request, 'subscriptions/subscription_form.html', {'form': form})

@login_required
def subscription_update(request, pk):
    """
    Handle form display and submission for updating an existing subscription.
    Only allow if the subscription belongs to the current user.
    """
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('subscriptions:list')
    else:
        form = SubscriptionForm(instance=subscription)

    return render(request, 'subscriptions/subscription_form.html', {'form': form})




def register_view(request):
    """
    Handle user registration using your custom UserCreationForm with Tailwind classes.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This creates the user
            messages.success(request, "Your account was created successfully!")
            # Optionally log the user in immediately
            auth_login(request, user)
            return redirect('subscriptions:list')  
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def my_login_view(request):
    
    if request.method == 'POST':
        
        form = MyLoginForm(request, data=request.POST)
        
        
        if form.is_valid():
            
            user = form.get_user()
            
            
            auth_login(request, user)
            
            
            return redirect('home')
    
    else:
        form = MyLoginForm(request)

    
    return render(request, 'registration/login.html', {'form': form})