import django_filters

from .models import *


"""class StudentCourseFilter(django_filters.FilterSet):
    pass
    student__id = django_filters.CharFilter(lookup_expr='iexact')
    course__code = django_filters.CharFilter(lookup_expr='iexact')
    overall__semester = django_filters.NumberFilter(field_name='overall_semester', lookup_expr='iexact')

    course_grade = django_filters.RangeFilter

    class Meta:
        model = StudentCourse
        fields = ['student_id ', 'course_code', 'course_grade', 'overall_semester']"""

