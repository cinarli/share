from django.shortcuts import render, redirect
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate,get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import resolve_url
from .functions import getSystemInfo
from .tasks import add_info
from django.conf import settings

User = get_user_model()

def register(request):
    
    if request.user.id:
        return redirect('empty:home')
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('accounts:login')
 
    else:
        f = UserCreationForm()
 
    return render(request, 'registration/register.html', {'form': f})

def logoutView(request):
    logout(request)
    return redirect('accounts:login')
class MyLoginView(LoginView):
    redirect_authenticated_user=reverse_lazy('empty:home')
    
    def get_success_url(self):
        url = self.get_redirect_url()
        info=getSystemInfo()
        add_info.apply_async(kwargs={'db':'users','col':'users_info','info':info})
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)