from django import forms
from .models import Subscription
from django.contrib.auth.forms import AuthenticationForm


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'cost', 'billing_cycle', 'next_renewal', 'category']


class MyLoginForm(AuthenticationForm):
    """
    Custom login form to add Tailwind classes or any extra fields/validation.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Tailwind classes to username/password fields
        self.fields['username'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        })
        
        # Optionally, if you want placeholders:
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = '••••••••'
