from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from mobile_api.ai_model import utils as ai_utils
from django.contrib.auth import login, logout
from main.utils import get_object_or_none
from mobile_api.models import *


def login_view(request):
    if request.user.is_authenticated:
        return redirect("website:home_page")
    
    error = None
    if request.method == "POST":
        user = get_object_or_none(User, username=request.POST.get('username'))
        if user and user.check_password(request.POST.get('password')):
            login(request, user)
            return redirect("website:home_page")
        else:
            error = "Wrong Username or Password!"
    
    context = {
        "error": error,
    }
    return render(request, "website/login.html", context)


def registration_view(request):
    if request.user.is_authenticated:
        return redirect("website:home_page")
    
    error = None
    if request.method == "POST":
        
        try:
            my_user = User.objects.create_user(
                username=request.POST.get('email').lower(),
                first_name=request.POST.get('name'),
                password=request.POST.get('password')
            )
            
            system_user = SystemUser.objects.create(
                phone=request.POST.get('phone'),
                birthday=request.POST.get('birthday'),
                gender=request.POST.get('gender'),
                user=my_user
            )
            login(request, my_user)
            return redirect("website:home_page")
        except Exception as e:
            error = "User Already Exists!"
    
    context = {
        "error": error, 
    }
    return render(request, "website/registration.html", context)


def logout_view(request):
    logout(request)
    return redirect("website:login_page")


@login_required(login_url="website:login_page")
def history_view(request):
    histories = SCDHistory.objects.filter(user=request.user)
    context = {
        "histories": histories
    }
    return render(request, 'website/history.html', context)


@login_required(login_url="website:login_page")
def home_view(request):
    result = False
    if request.method == "POST":
        # create record in database
        scd_history = SCDHistory.objects.create(
            image=request.FILES.get('image'),
            user=request.user
        )
        # send image path to the AI model to predict the disease
        result = ai_utils.predict_cancer_disease(scd_history.image.path)
        # save the predicated disease in the database
        scd_history.diagnose = result
        scd_history.save()
    
    data = {
        "result": result,
    }
    return render(request, "website/home.html", context = data)

