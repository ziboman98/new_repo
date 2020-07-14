from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import User

# Create your models here.


# Model for Department
class Department(models.Model):
    department_name = models.CharField(max_length=100, default='Computer Science', primary_key=True)

    def __str__(self):
        return self.department_name


# Model for Programme
class Programme(models.Model):
    plan_code = models.CharField(max_length=6, default='BSc###', primary_key=True)
    plan_name = models.CharField(max_length=200)
    overall_program_credits = models.PositiveIntegerField(default=120)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programme_dept')

    class Meta:
        ordering = ['plan_code']

    def __str__(self):
        return self.plan_name


# Students model
class Student(models.Model):
    REASON = (
        ('Fail and Discontinue', 'Fail and Discontinue'),
        ('Health Reasons', 'Health Reasons'),
        ('Fail and Exclude', 'Fail and Exclude'),
        ('Continuing Student', 'Continuing Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    student_id = models.CharField(max_length=9, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='student_programme')
    reason_for_leaving = models.CharField(max_length=100, choices=REASON, default='Fail and Discontinue')
    semesters_passed = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        ordering = ['student_id']

    def __str__(self):
        return self.student_id


# # StudentProgram model
# class StudentProgram(models.Model):
#     student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='studentProg_studentID')
#     plan_code = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='stuProg_planCode')
#
#     def __str__(self):
#         return '%s %s' % (self.student_id, self.plan_code)


# # Semester model
# class Semester(models.Model):
#     semester_credits = models.PositiveIntegerField(default=15)
#     overall_semester = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return self.semester_type

# Program Semester model

class ProgramSemester(models.Model):
    plan_code = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='progSem_planCode')
    overall_semester = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    total_credits = models.PositiveIntegerField(default=15)

    class Meta:
        ordering = ['plan_code']

    def __str__(self):
        return '%s %s' % (self.plan_code, self.overall_semester)


# Course model
class Course(models.Model):
    COURSETYPE = (
        ('Core', 'Core'),
        ('Optional', 'Optional'),
        ('GEC', 'GEC'),
        ('Elective', 'Elective'),
    )
    SEMESTER = (
        ('1', '1'),
        ('2', '2'),
        ('Winter semester', 'Winter semester'),
    )
    course_code = models.CharField(max_length=6, primary_key=True)
    course_title = models.CharField(max_length=200)
    course_type = models.CharField(max_length=9, choices=COURSETYPE, default='Core')
    credits = models.PositiveIntegerField(default=3, validators=[MinValueValidator(3), MaxValueValidator(4)])
    prerequisite = models.CharField(max_length=20, blank=True)
    semester_type = models.CharField(max_length=100, default='1', choices=SEMESTER)
    level = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(4)])
    overall_semester = models.ForeignKey(ProgramSemester, on_delete=models.CASCADE, related_name='course_overallSem')
    programme = models.ManyToManyField(Programme)
    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return self.course_code


# StudentCourse model
class StudentCourse(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="usercourses")
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE,related_name="mycourse")
    course_grade = models.PositiveIntegerField(default=50)
    GPA = models.FloatField(default=2.00, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], blank=True)
    # semester_type = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='StudentCourse_semesterType')
    overall_semester = models.ForeignKey(ProgramSemester, on_delete=models.CASCADE,
                                         related_name='StudentCourse_overall_semester')

    class Meta:
        ordering = ['student_id']
    def __str__(self):
        return '%s %s' % (self.student_id, self.course_code)


# StudentCGPA
# class StudentCGPA(models.Model):
#     student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
#     CGPA = models.FloatField(default=2.00, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
#
#     class Meta:
#         ordering = ['student_id']
#
#     def __str__(self):
#         return '%s %s' %  (self.student_id, self.CGPA)

# ProgramCourse model
class ProgramCourse(models.Model):
    plan_code = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='progCourse_planCode')
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='PlanCourse_course_code')
    def __str__(self):
        return self.overall_semester

