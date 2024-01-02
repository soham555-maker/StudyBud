from django.urls import path
from . import views

urlpatterns = [
    path('login-page/', views.loginPage, name='login-page'),
    path('logout-page/', views.logoutPage, name='logout-page'),
    path('register-page/', views.registerPage, name='register-page'),

    path('', views.home, name='home'),
    path('profile-page/<int:pk>/', views.profilePage, name='profile-page'),

    path('about/', views.about, name='about'),
    path('room/<int:pk>/', views.room, name='room'),
    
    path('create-room/', views.createRoom, name='create-room'),
    
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<int:pk>/', views.deleteMessage, name='delete-message'),
    
]
