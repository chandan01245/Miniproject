from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .form import medication_form, register_form
from .models import register
from .qr_generator import qr_gen


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("Password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in"))
            return redirect('dashboard',{'user':username})
        else:
            messages.success(request,("Invalid password. PLease try again"))
            return redirect('login')
    else:
        return render(request,"Login.html")
    
def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out"))
    return redirect('login')

@login_required
def user_dashboard(request):
    submitted = False
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Dashboard?submitted=True')
        else:
            print("Form errors:", form.errors)
    else:
        form = register_form()
        if 'submitted' in request.GET:
            submitted = True
    user_list = register.objects.all()
    user_count = register.objects.all().count()
    return render(request,"Dashboard.html",{'user_list':user_list,'user_count':user_count})

@login_required
def user_registeration(request):
    submitted = False
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,("New patient registered"))
            return HttpResponseRedirect('/Registeration?submitted=True')
        else:
            print("Form errors:", form.errors)
    else:
        form = register_form()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,"register.html",{'current_path': request.path})

@login_required
def user_appointment(request):
    user_list = register.objects.all()
    return render(request,"appointments.html",{'current_path': request.path ,'user_list':user_list})

@login_required
def prescription(request):
    submitted = False
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = medication_form(request.POST)
        if form.is_valid():
            instance = form.save()
            print("Saved instance:", instance)
            formMail = instance.email
            formdata = instance.Medication
            print("Calling qr_gen with:", formMail, formdata)
            qr_gen(formMail,formdata)
            messages.success(request,("Mail sent Succesfully"))
            return HttpResponseRedirect('/prescription?submitted=True')
        else:
            print("Form errors:", form.errors)
    else:
        form = medication_form()
        
        if 'submitted' in request.GET:
            submitted = True
    return render(request,"prescription.html",{'current_path': request.path})

def load_vending_machine(request):
    if request.method == 'POST':
        qr_code = request.POST.get("qrCode")
        
        print("QR Code: ",qr_code)
        return HttpResponse("Backend Response: "+qr_code)

    return render(request,"VendingMachine.html")

def error_page(request):
    return render(request,'error.html')