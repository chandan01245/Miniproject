from datetime import datetime
from django.core.validators import EmailValidator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .form import medication_form, register_form
from .models import appointment, register
from .mongodb import save_appointment
from .qr_generator import qr_gen


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("Password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['username'] = username
            messages.success(request,("You have been logged in"))
            return redirect("dashboard")
        else:
            messages.error(request,("Invalid password. PLease try again"))
            return redirect('login')
    else:
        return render(request,"Login.html")
    
def logout_user(request):
    logout(request)
    request.session.flush()
    messages.success(request,("You have been logged out"))
    return redirect('login')

@login_required
def user_dashboard(request):
    submitted = False
    today = datetime.today().date()
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = register_form(request.POST)
        if form.is_valid():
            new_register = form.save()
            save_appointment(new_register)
            return HttpResponseRedirect('/Dashboard?submitted=True')
        else:
            print("Form errors:", form.errors)
    else:
        form = register_form()
        if 'submitted' in request.GET:
            submitted = True
    user_list = register.objects.all()
    user_count = register.objects.all().count()
    username = request.session.get('username', 'Guest')
    return render(request,"Dashboard.html",{'user_list':user_list,'user_count':user_count,'user':username,'today':today})

@login_required
def user_registration(request):
    submitted = False
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = register_form(request.POST)
        if form.is_valid():
            new_register = form.save()
            messages.success(request,("New patient registered"))
            save_appointment(new_register)
            return HttpResponseRedirect('/Registration?submitted=True')
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
    today = datetime.today().date()
    return render(request,"appointments.html",{'current_path': request.path ,'user_list':user_list,'today':today})

@login_required
def search_bar(request):
    today = datetime.today().date()
    if request.method == 'POST':
        searched = request.POST.get('Search')
        names = register.objects.filter(name__contains=searched)
    return render(request,"search.html",{'searched':names,'today':today})

def delete_appointment(request,id):
    today = datetime.today().date()
    appointment_id = register.objects.get(pk=id)
    appointment_id.delete()
    messages.success(request,("Deleted Appointment"))
    user_list = register.objects.all()
    return render(request,"appointments.html",{'current_path': request.path ,'user_list':user_list,'today':today})

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
            dosage = instance.Dosage
            frequency = instance.frequency
            notes = instance.additional_notes
            print("Calling qr_gen with:", formMail, formdata)
            qr_gen(formMail,formdata,dosage,frequency,notes)
            messages.success(request,("Mail sent Successfully"))
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
