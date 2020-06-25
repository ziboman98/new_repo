from django.contrib import admin
from . models import *
# Register your models here.

admin.site.site_header = 'Returning Students Credits Checking System Admin Dashboard'
admin.site.register(Department)
admin.site.register(Programme)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(ProgramSemester)
admin.site.register(StudentCourse)
admin.site.register(StudentCGPA)

# admin.site.register()