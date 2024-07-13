from django.shortcuts import get_object_or_404, render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView,ListView
from django.urls import reverse_lazy
from django.http import  HttpResponseRedirect
from django.contrib.auth import  logout,login
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from core.views import menufunc
from core.models import *
class LoginUser(LoginView):
    form_class=LoginUserForm
    template_name="core/login.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        context['title'] = "LogIn"
        return context 
    
    def get_success_url(self):
        return reverse_lazy('home')
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

class RegisterUser(CreateView):
    form_class=RegisterUserForm
    template_name='core/register.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        context['title'] = "Register"
        return context
    
    success_url=reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class ProfileUser(LoginRequiredMixin,UpdateView):
    model=get_user_model()
    form_class=ProfileUserForm
    template_name="core/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        context['title'] = "ProFile"
        return context
    
    def get_success_url(self):
        return reverse_lazy('users:profile')
    def get_object(self, queryset=None):
        return self.request.user

class Kabinet(ListView):
    model=Maqola
    template_name="core/kabinet.html"
    title_page="Kabinet"
    context_object_name="posts"
    def get_queryset(self):
        # Ensure we are only processing for authenticated users
        if self.request.user.is_authenticated:
            return Maqola.objects.filter(author=self.request.user)
        return Maqola.objects.none()  # Return empty queryset for non-authenticated users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        # Only add counts for authenticated users
        if self.request.user.is_authenticated:
             context['umumiy_maqolalar']=Maqola.objects.filter(author=self.request.user).count()
             context['chop_etilgan_maqolalar']=Maqola.objects.filter(author=self.request.user,is_published=True).count()
             context['rad_etilgan_maqolalar']=Maqola.objects.filter(author=self.request.user,rejection=True).count()
        else:
           context['umumiy_maqolalar']=0
           context['chop_etilgan_maqolalar']=0
           context['rad_etilgan_maqolalar']=0
        return context


