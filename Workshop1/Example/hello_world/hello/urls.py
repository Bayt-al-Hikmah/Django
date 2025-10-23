from django.urls import path
from .import views

urlpatterns = [
    path('', views.hello_view, name='hello'),
    path('<str:name>/', views.personal_greeting, name='personal_greeting'),
]