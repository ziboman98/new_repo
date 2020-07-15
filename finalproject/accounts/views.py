from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *

from fpdf import FPDF, HTMLMixin

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
@login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def home(request):
	context = {}
	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def landingPage(request):
    context = {}
    return render(request, 'accounts/index.html', context)
# registerPage
# @unauthenticated_user
# @allowed_users(allowed_roles=['admin'])
# @admin_only
@unauthenticated_user
def registerPage(request):
    """This is the function that allows users to be registered into the system by the admin"""
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
    """This is the function that allows users to be logged in"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,'Username or Password is incorrect')

    context = {}
    return render(request,'accounts/login.html', context)

# Logging out users
def logoutUser(request):
    """This is the function that allows users to be logged out"""
    logout(request)
    return redirect('login')



# @login_required(login_url='login')
# @allowed_users(allowed_roles=['student', 'admin'])
def graduation(request):
    """This function checks whether the student fulfills all the requirements for graduation"""
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

    # len on f should be equal or greater than the len of courses_complete to graduate
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
    """This function displays the courses which a student has gotten a grade of
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
    """This function displays the courses which a student has not passed wit grade of
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
    """This function determines the amount of semesters left for a user"""
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
    print(total_credits)
    sem_done = math.floor(total_credits/15)
    programme_ = student.programme
    whatsleft = 8 - sem_done
    if whatsleft < 0 :
        whatsleft = 0
    whatsleft = math.floor(whatsleft)
    semestersDone = int(programme_.overall_program_credits)/15
    how_many_semester_left = math.floor(semestersDone)
    context = {'semester_left':how_many_semester_left, 'whatsleft':whatsleft,'sem_done': sem_done, 'total':total_credits}
    return render(request, "accounts/semester.html", context)


# class HelloPDFView(PDFTemplateView):
#     template_name = 'semester.html'

class HtmlPdf(FPDF,  HTMLMixin):
    pass

def print_pdf(request):
    pdf = HtmlPdf()
    pdf.add_page()
    pdf.write_html(render_to_string('accounts/pdf.html'))

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'

    return response

def grad_pdf(request):
    pdf = HtmlPdf()
    pdf.add_page()
    pdf.write_html(render_to_string('accounts/grad_pdf.html'))

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'

    return response

def completed_pdf(request):
    pdf = HtmlPdf()
    pdf.add_page()
    pdf.write_html(render_to_string('accounts/completed_pdf.html'))

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'

    return response

def semester_pdf(request):
    pdf = HtmlPdf()
    pdf.add_page()
    pdf.write_html(render_to_string('accounts/semester_pdf.html'))

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'

    return response

def incomplete_pdf(request):
    pdf = HtmlPdf()
    pdf.add_page()
    pdf.write_html(render_to_string('accounts/incomplete_pdf.html'))

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'

    return response

def complete_pdf(request):
    pdf = HtmlPdf()
    pdf.add_page()
    pdf.write_html(render_to_string('accounts/complete_pdf.html'))

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'

    return response

# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('semester.html')
#         context = {
#             "sem_done": 2,
#             "whatsleft": 6,
#         }
#         html = template.render(context)
#         return HttpResponse(html)













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