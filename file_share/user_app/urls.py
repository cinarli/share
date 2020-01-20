
from django.urls import path
from .views import  register,MyLoginView,logoutView
from django.contrib.auth.views import LogoutView
app_name='user_app'
urlpatterns = [
    path('register/', register, name = 'register'),
    path('login/', MyLoginView.as_view(), name = 'login'),
    path('logout/', logoutView, name='logout'),
]
