from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .form import medication_form, register_form
from .models import appointment, register
from .qr_generator import qr_gen


# Create your views here.
@login_required
def test_view(request):
    print(f"Is authenticated: {request.user.is_authenticated}")
    print(f"User: {request.user}")
    return HttpResponse("You are logged in.")

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("Password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in"))
            request.session['username'] = username
            return redirect("dashboard")
        else:
            messages.success(request,("Invalid password. PLease try again"))
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
    username = request.session.get('username', 'Guest')
    return render(request,"Dashboard.html",{'user_list':user_list,'user_count':user_count,'user':username})

@login_required
def user_registration(request):
    submitted = False
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,("New patient registered"))
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
    return render(request,"appointments.html",{'current_path': request.path ,'user_list':user_list})

def delete_appointment(request,id):
    appointment_id = register.objects.get(pk=id)
    appointment_id.delete()
    messages.success(request,("Deleted Appointment"))
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