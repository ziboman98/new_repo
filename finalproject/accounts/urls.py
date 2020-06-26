from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('graduation/', views.graduation, name="graduation"),
    path('incomplete/', views.incomplete_courses, name="incompleteSemesters"),
    path('complete/', views.complete_courses, name="completeSemesters"),
    path('semester/', views.semester, name="semester"),
    path('incomplete/', views.incomplete_courses, name="incompleteSemesters"),

]