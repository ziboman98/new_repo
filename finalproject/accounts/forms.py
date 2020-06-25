from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# The create user form class which is used to create a user in the system
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']