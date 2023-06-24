from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('register/', views.register, name='register'),
]
