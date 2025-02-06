from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subscription
from .forms import SubscriptionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .forms import MyLoginForm
from .forms import CustomUserCreationForm
from .utils import send_welcome_email
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ReminderEmailForm

@login_required
def subscription_list(request):
    """
    List all subscriptions for the currently logged-in user.
    """
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})

@login_required
def subscription_detail(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    form = ReminderEmailForm(initial={'custom_email': request.user.email})
    return render(request, 'subscriptions/subscription_detail.html', {
        'subscription': subscription,
        'form': form,
    })

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
            user = form.save()  # This now saves the email as well
            # Immediately send a welcome email
            send_welcome_email(user.email)
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



def send_reminder_view(request, pk):
    if request.method == 'POST':
        subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
        
        # 1. Get the custom email from the form input
        recipient_email = request.POST.get('custom_email')
        if not recipient_email:
            messages.error(request, "Please provide a valid email address.")
            return redirect('subscriptions:detail', pk=pk)

        # 2. Get the reminder offset from the form input.
        reminder_days_str = request.POST.get('reminder_days')
        if reminder_days_str:
            try:
                reminder_days = int(reminder_days_str)
            except ValueError:
                reminder_days = subscription.reminder_days  # fallback to current value if conversion fails
        else:
            reminder_days = subscription.reminder_days  # use the stored value if nothing is submitted

        # Optionally, update the subscription with the new reminder preference
        subscription.reminder_days = reminder_days
        subscription.save()

        # 3. Build the subject & message incorporating the chosen offset.
        subject = f"Reminder: {subscription.name} renewal approaching!"
        message = (
            f"Hello,\n\n"
            f"This is a reminder that your subscription to {subscription.name} is set to renew on {subscription.next_renewal}.\n"
            f"You chose to be reminded {reminder_days} days in advance.\n"
            f"Cost: ${subscription.cost}\n\n"
            "Thank you for using Subscription Manager!"
        )
        from_email = settings.DEFAULT_FROM_EMAIL

        # 4. Send the email.
        send_mail(
            subject,
            message,
            from_email,
            [recipient_email],
            fail_silently=False,
        )

        # 5. Show success and redirect.
        messages.success(request, f"Reminder email sent to {recipient_email}!")
        return redirect('subscriptions:detail', pk=pk)
    
    return redirect('subscriptions:list')