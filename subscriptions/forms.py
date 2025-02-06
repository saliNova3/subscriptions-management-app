from django import forms
from .models import Subscription
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': (
                'bg-gray-50 border border-gray-300 text-gray-900 '
                'dark:bg-gray-700 dark:border-gray-600 dark:text-white '
                'block w-full p-2.5 focus:ring-blue-500 focus:border-blue-500 '
            ),
            'placeholder': 'Your Username',
        })

        self.fields['password'].widget.attrs.update({
            'class': (
                'bg-gray-50 border border-gray-300 text-gray-900 '
                'dark:bg-gray-700 dark:border-gray-600 dark:text-white '
                'block w-full p-2.5 focus:ring-blue-500 focus:border-blue-500 '
            ),
            'placeholder': '••••••••',
        })


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': (
                'bg-gray-50 border border-gray-300 text-gray-900 '
                'dark:bg-gray-700 dark:border-gray-600 dark:text-white '
                'block w-full p-2.5 '
                'focus:ring-blue-500 focus:border-blue-500 '
                'placeholder-gray-400'
            ),
            'placeholder': 'Your email'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_classes = (
            'bg-gray-50 border border-gray-300 text-gray-900 '
            'dark:bg-gray-700 dark:border-gray-600 dark:text-white '
            'block w-full p-2.5 '
            'focus:ring-blue-500 focus:border-blue-500 '
            'placeholder-gray-400'
        )

        self.fields['username'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Your username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Create password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Confirm password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class ReminderEmailForm(forms.Form):
    custom_email = forms.EmailField(
        label="Enter an email to receive reminder",
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@domain.com',
            'class': 'w-full text-black hover:bg-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5'
        })
    )       