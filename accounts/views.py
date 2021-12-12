from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
 
 
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class MyPageView(generic.CreateView):
    model = User