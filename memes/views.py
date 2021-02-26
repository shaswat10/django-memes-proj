from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse  
import json
import requests
import random 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from . import models
# Create your views here.



#########Registeration page for user registration #########
def user_registration(request):
    form = forms.CreateUserForm()

    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('../login')

    context = {'form':form}
    return render(request, 'memes/registration.html', context)




##############user login page########
def loginPage(request):

    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) ### taking user id & pass
         
        
        
        if user is not None:  ## if user is valid
            login(request, user)
            response = HttpResponse("Cookie Set")
            return redirect('../cookie')

        else:
            messages.error(request, 'Wrong Credentials!')
        
    return render(request, 'memes/login.html')



########### Cookie page This page lets the use to accept or reject cookie###############
@login_required
def cookie(request):


    if request.COOKIES.get('name'):
        obj = models.User.objects.get(username = request.COOKIES['name'])


        login(request, user=obj)
   
        return redirect('../memes')


    else:

        print("--------------------------------------------------")
        print("none")
        respones = render(request,'memes/cookie.html')
        print(request.session.test_cookie_worked())

        if 'reject_btn' in request.POST:   #### if user rejects the storing of cookies
            print("-----------reject")
            obj = models.UserConsentModel(user=request.user, concent = False)
            obj.save()
            return redirect('../logoutpage')
        
        elif 'accept_btn' in request.POST:  #### if user accepts the storing of cookies
            print("-----------accept")
            obj = models.UserConsentModel(user=request.user, concent = True)
            obj.save()
            respones = redirect('../memes') 
            respones.set_cookie('name',request.user)
            return respones
            return redirect('../memes')


    return respones



def meme_view(request):
    # print("here")
    if request.COOKIES.get('name'):
        obj = models.User.objects.get(username = request.COOKIES['name'])
        login(request, user=obj)
        # login(request, username= request.COOKIES['name'].username, password= request.COOKIES['name'].password)
            
    ########### retriving data from api and extracting random five records to get displayed 
        response = requests.get('https://api.imgflip.com/get_memes') 
        data = response.json()
        print(type(data))
        print(request.user)

        meme  = data["data"]
        meme_list = meme["memes"]


        name_lst=[]
        url_lst=[]

        for val in range(5):
            name_lst.append(meme_list[val]["name"])
            url_lst.append(meme_list[val]["url"])

        memes = random.sample(meme_list, 5)
    ###################################################################################################

    
        context = {'memes':memes}

        return render(request, 'memes/memepage.html', context)

    else:
        return redirect('../login')



# def setcookies(request):

#     respones = HttpResponse("Cookie Set")  
#     respones.set_cookie('name',request.user)
#     return respones

# def getcookies(request):
#     print(request.COOKIES['name'])
#     return render(request,'memes/test2.html')


def logout_view(request):
    logout(request)
    respones = redirect('../login') 
    respones.delete_cookie('name')
    return respones
 