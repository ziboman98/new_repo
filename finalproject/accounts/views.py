from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *

from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML
import tempfile

# Create your views here.

# Home view
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def home(request):
	context = {}
	return render(request, 'accounts/dashboard.html', context)

# registerPage
# @unauthenticated_user
# @allowed_users(allowed_roles=['admin'])
# @admin_only

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('student_id')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            messages.success(request, 'Account was created for '+username)
            return redirect('login')

    context = {'form':form}
    return render(request,'accounts/register.html',context)

# Login View
@unauthenticated_user
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

# Logging out users
def logoutUser(request):
    logout(request)
    return redirect('login')


# converting HTML to pdf
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def generate_graduation_pdf(request):
    # return render(request, 'accounts/graduation.html')
    pass

# converting HTML to pdf
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def generate_incomplete_pdf(request):
    # return render(request, 'accounts/incomplete.html')
    pass

# converting HTML to pdf
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def generate_complete_pdf(request):
    # return render(request, 'accounts/complete.html', context)
    pass

# converting HTML to pdf
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def generate_semester_pdf(request):
    # return render(request, 'accounts/semester.html')
    pass


def complete_courses(request):
    try:
        student = get_object_or_404(Student,user = request.user)
        courses_complete = student.usercourses.all().filter(course_grade__gte=50)
        courses_incomplete = student.usercourses.all().filter(course_grade__lt=50)
    except Exception:
        messages.error('no course complete')
    context = {'courses_complete': courses_complete,'courses_incomplete':courses_incomplete}
    return render(request, "accounts/complete.html", context)


def incomplete_courses(request):
    student = get_object_or_404(Student,user = request.user)
    student_programm = student.programme.all()
    #allcourses =
    courses_complete = student.usercourses.all().filter(course_grade__gte=50)
    print (student_programm)
    print("hg")

    #return render(request, "accounts/incomplete.html", {'student':student_programm})

