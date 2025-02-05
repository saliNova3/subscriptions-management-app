from django.urls import path
from . import views 

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscription_list, name='list'),
    path('create/', views.subscription_create, name='create'),
    path('<int:pk>/', views.subscription_detail, name='detail'),
    path('<int:pk>/update/', views.subscription_update, name='update'),
    path('<int:pk>/send_reminder/', views.send_reminder_view, name='send_reminder'),
]
