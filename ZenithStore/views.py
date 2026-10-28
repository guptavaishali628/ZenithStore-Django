# import httpresponse
from django.http import HttpResponse
from django.shortcuts import render

# create function
def home(request):
    # return HttpResponse("Welcome to ZenithStore")
    return render(request,'home.html')
