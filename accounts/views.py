from django.shortcuts import render
from .forms import RegistrationForm

# Create your views here.

# create register function
def register(request):
    form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

# create login function
def login(request):
    return render(request, 'accounts/login.html')

# create logout function
def logout(request):
    return render(request, 'accounts/logout.html')
