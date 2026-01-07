from django.urls import path
from .views import UserProfileView, UpdateUserView, UpdatePasswordView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('update/', UpdateUserView.as_view(), name='user-update'),
    path('update-password/', UpdatePasswordView.as_view(), name='user-update-password'),
]