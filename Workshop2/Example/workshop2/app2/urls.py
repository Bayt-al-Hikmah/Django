from django.urls import path
from . import views

urlpatterns = [
    path('<str:role>/', views.index, name='index'),
]