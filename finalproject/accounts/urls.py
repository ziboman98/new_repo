from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('graduation/', views.generate_graduation_pdf, name="graduation"),
    path('incomplete/', views.generate_incomplete_pdf, name="incompleteSemesters"),
    path('complete/', views.complete_courses, name="completeSemesters"),
    path('semester/', views.generate_semester_pdf, name="semester"),
    path('incomplete/', views.incomplete_courses, name="incompleteSemesters"),

]