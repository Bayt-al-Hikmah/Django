from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_feedback, name='submit_feedback'),
    path('feedbacks/', views.feedback_list, name='feedbacks'),
]