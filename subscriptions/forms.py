from django import forms
from .models import Subscription
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'cost', 'billing_cycle', 'next_renewal', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
                'placeholder': 'Subscription Name'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
                'placeholder': 'Monthly cost (e.g. 9.99)'
            }),
            'billing_cycle': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
            }),
            'next_renewal': forms.DateInput(attrs={
                'type': 'date',  # so browsers show a date picker
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
            }),
            'category': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
            }),
        }


class MyLoginForm(AuthenticationForm):
    """
    Custom login form to add Tailwind classes or any extra fields/validation.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Username Field
        self.fields['username'].widget.attrs.update({
            'class': (
                'bg-gray-50 border border-gray-300 text-gray-900 '
                'dark:bg-gray-700 dark:border-gray-600 dark:text-white '
                'block w-full p-2.5 focus:ring-blue-500 focus:border-blue-500'
            ),
            'placeholder': 'Your Username',
        })

        # Password Field
        self.fields['password'].widget.attrs.update({
            'class': (
                'bg-gray-50 border border-gray-300 text-gray-900 '
                'dark:bg-gray-700 dark:border-gray-600 dark:text-white '
                'block w-full p-2.5 focus:ring-blue-500 focus:border-blue-500'
            ),
            'placeholder': '••••••••',
        })


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 dark:bg-gray-700 dark:border-gray-600 dark:text-white block w-full p-2.5',
            'placeholder': 'Your username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 dark:bg-gray-700 dark:border-gray-600 dark:text-white block w-full p-2.5',
            'placeholder': 'Create password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 dark:bg-gray-700 dark:border-gray-600 dark:text-white block w-full p-2.5',
            'placeholder': 'Confirm password'
        })