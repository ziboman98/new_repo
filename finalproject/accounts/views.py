from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm

# Create your views here.

# Home view
def home(request):
	context = {}
	return render(request, 'accounts/dashboard.html', context)

# registerPage
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #group = Group.objects.get(name='customer')
            #user.groups.add(group)
            messages.success(request, 'Account was created for '+username)
            return redirect('login')


    context = {'form':form}
    return render(request,'accounts/register.html',context)

# Login View
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')

    context = {}
    return render(request,'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



