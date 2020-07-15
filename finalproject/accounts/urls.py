from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from accounts import views as web_views

from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('graduation/', views.graduation, name="graduation"),
    path('incomplete/', views.incomplete_courses, name="incompleteSemesters"),
    path('complete/', views.complete_courses, name="completeSemesters"),
    path('index/',views.landingPage, name="index"),
    # path('semester/', PDFTemplateView.as_view(template_name='accounts/semester.html',
    #                                        filename='my_pdf.pdf'), name='semester'),
    path('semester/', views.semester, name="semester"),
    # path('incomplete/', views.incomplete_courses, name="incompleteSemesters"),
    path(
        "pdf/",
        web_views.print_pdf,
        name="pdf",
    ),

path(
        "semester_pdf/",
        web_views.semester_pdf,
        name="semester_pdf",
    ),

    path(
            "grad_pdf/",
            web_views.grad_pdf,
            name="grad_pdf",
        ),

    path(
            "incomplete_pdf/",
            web_views.incomplete_pdf,
            name="incomplete_pdf",
        ),

    path(
            "complete_pdf/",
            web_views.complete_pdf,
            name="complete_pdf",
        ),

    path(
            "completed_pdf/",
            web_views.completed_pdf,
            name="completed_pdf",
        ),

    # path to reset email form
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name='reset_password'),

    # email sent success message
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    # link to password reset form in mail
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name='password_reset_confirm'),

    # password successfully changed message
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),
]