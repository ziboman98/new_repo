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
    programme_credits = 120
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
    # print(programme_)
    # print(coursesInMyProgramme)
    message = False
    if len(f) >= len(courses_complete) and total_credits > 120:
        message = True
    else:
        pass

    # get all the courses programme requires

    context = {'message': message, 'programme_credits': programme_credits}
    return render(request, 'accounts/graduation.html', context)


# @login_required(login_url='login')
def complete_courses(request):
    """This method displays the courses which a student has gotten a grade of
        50 or more.
    """
    try:
        student = get_object_or_404(Student,user = request.user)
        courses_complete = student.usercourses.all().filter(course_grade__gte=50)
        courses = student.usercourses.all().filter(course_grade__gte=50).values('course_code')

        # courses_incomplete = student.usercourses.all().filter(course_grade__lt=50)
    except Exception:
        messages.error('no course complete')
    context = {'courses_complete': courses_complete}
    return render(request, "accounts/complete.html", context)

# converting HTML to pdf
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def incomplete_courses(request):
    """This method displays the courses which a student has not passed wit grade of
           50 and above or has never taken.
       """
    try:
        student = get_object_or_404(Student, user=request.user)
        # courses_complete = student.usercourses.all().filter(course_grade__gte=50)
        courses_complete = student.usercourses.all().filter(course_grade__gte=50).values('course_code')
        programme_ = student.programme
        coursesInMyProgramme = Course.objects.filter(programme__plan_code=programme_.plan_code).values('course_code')
        print(coursesInMyProgramme)
        lst = []
        for i in coursesInMyProgramme:
            if i not in courses_complete:
                lst.append(i)


    except Exception:
        messages.error('No course incomplete')
    context = {'courses_incomplete': lst}
    return render(request, "accounts/incomplete.html", context)


# converting HTML to pdf
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])



def semester(request):
    """This functions determines the amount of semesters left for a user"""
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
    whatsleft = (120 - int(programme_.overall_program_credits))/15
    whatsleft = math.floor(whatsleft)
    semestersDone = int(programme_.overall_program_credits)/15
    how_many_semester_left = math.floor(semestersDone)
    context = {'semester_left':how_many_semester_left, 'whatsleft':whatsleft}
    return render(request, "accounts/semester.html", context)

#  """arr = []
#         for i in courses_complete:
#             for j in Course.objects.all():
#                 if i.course_code == j:
#                     arr.append(j)
#         total_credits = 0
#         for i in arr:
#             total_credits+=i.credits
#
#         print(student)
#         print(total_credits)
#
#         programme_ = student.programme
#         coursesInMyProgramme = Course.objects.filter(programme__plan_code=programme_.plan_code)
#
#         f = set()
#
#         for i in coursesInMyProgramme:
#             f.add(i)
#         for i in courses_complete:
#             f.add(i)
#
#         # len on f should be equal to the len of courses_complete to graduate
#         if len(f) < len(courses_complete) and total_credits > 120:
#             print("graduate!")
#         else:
#             print("no")
# """
#         """for i in courses:
#             credits =+ i.credits
#         print(credits)"""