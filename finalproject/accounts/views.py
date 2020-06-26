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
import math
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
def graduation(request):
    """This method checks whether the student fulfills all the requirements for graduation"""
    student = get_object_or_404(Student, user=request.user)
    courses_complete = student.usercourses.all().filter(course_grade__gte=50)
    arr = []
    for i in courses_complete:
        for j in Course.objects.all():
            if i.course_code == j:
                arr.append(j)
    total_credits = 0
    for i in arr:
        total_credits += i.credits

    programme_ = student.programme
    coursesInMyProgramme = Course.objects.filter(programme__plan_code=programme_.plan_code)

    f = set()

    for i in coursesInMyProgramme:
        f.add(i)
    for i in courses_complete:
        f.add(i)

    # len on f should be equal to the len of courses_complete to graduate


    print(programme_)
    print(coursesInMyProgramme)

    if len(f) < len(courses_complete) and total_credits > 120:
        print("graduate!")
    else:
        print("no")




    # get all the courses programme requires

    context = {'courses_complete': courses_complete, 'programme_credits': programme_credits}
    return render(request, 'accounts/graduation.html', context)
    # pass


# @login_required(login_url='login')
def complete_courses(request):
    """This method displays the courses which a student has gotten a grade of
        50 or more.
    """
    try:
        student = get_object_or_404(Student,user = request.user)
        courses_complete = student.usercourses.all().filter(course_grade__gte=50)
        courses = student.usercourses.all().filter(course_grade__gte=50).values('course_code')
        """arr = []
        for i in courses_complete:
            for j in Course.objects.all():
                if i.course_code == j:
                    arr.append(j)
        total_credits = 0
        for i in arr:
            total_credits+=i.credits

        print(student)
        print(total_credits)

        programme_ = student.programme
        coursesInMyProgramme = Course.objects.filter(programme__plan_code=programme_.plan_code)

        f = set()

        for i in coursesInMyProgramme:
            f.add(i)
        for i in courses_complete:
            f.add(i)

        # len on f should be equal to the len of courses_complete to graduate
        if len(f) < len(courses_complete) and total_credits > 120:
            print("graduate!")
        else:
            print("no")
"""
        """for i in courses:
            credits =+ i.credits
        print(credits)"""
        # courses_incomplete = student.usercourses.all().filter(course_grade__lt=50)
    except Exception:
        messages.error('no course complete')
    context = {'courses_complete': courses_complete}
    return render(request, "accounts/complete.html", context)





# converting HTML to pdf
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def incomplete_courses(request):
    # student = get_object_or_404(Student,user = request.user)
    # programme = 
    # student_programme = student.programme.all()
    # programme_courses =  
    # courses_complete = student.usercourses.all().filter(course_grade__null=True)
    # print (student_programm)
    # print("hg")
    #return render(request, "accounts/incomplete.html", {'student':student_programm, 'courses_incomplete':courses_incomplete})

    pass

# converting HTML to pdf
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def generate_semester_pdf(request):
    # return render(request, 'accounts/semester.html') 
    pass


def semester(request):

    student = get_object_or_404(Student, user=request.user)
    courses_complete = student.usercourses.all().filter(course_grade__gte=50)
    arr = []
    for i in courses_complete:
        for j in Course.objects.all():
            if i.course_code == j:
                arr.append(j)
    total_credits = 0
    for i in arr:
        total_credits += i.credits
    programme_ = student.programme
    how_many_semester_left = int(programme_.overall_program_credits)/15
    how_many_semester_left = math.floor(how_many_semester_left)
    context = {'semester_left':how_many_semester_left,'programme':programme_}
    return render()

