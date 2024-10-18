from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def login_data(request):
    return render(request,"login.html")

def dashboard_data(request):
    return render(request, 'Dashboard.html')