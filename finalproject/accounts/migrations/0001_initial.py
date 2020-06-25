# Generated by Django 3.0.7 on 2020-06-17 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('course_title', models.CharField(max_length=200)),
                ('core_type', models.CharField(choices=[('Core', 'Core'), ('Optional', 'Optional'), ('Elective', 'Elective')], default='Core', max_length=9)),
                ('credits', models.PositiveIntegerField(default=3)),
                ('prerequisite', models.CharField(blank=True, max_length=20)),
                ('semester_type', models.CharField(choices=[('1', '1'), ('2', '2')], default='1', max_length=9)),
                ('level', models.PositiveIntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_name', models.CharField(default='Computer Science', max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('plan_code', models.CharField(default='BSc###', max_length=6, primary_key=True, serialize=False)),
                ('plan_name', models.CharField(max_length=200)),
                ('department_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programme_dept', to='accounts.Department')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_semester', models.PositiveIntegerField(default=1)),
                ('total_credits', models.PositiveIntegerField(default=15)),
                ('plan_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progSem_planCode', to='accounts.Programme')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('reason_for_leaving', models.CharField(choices=[('Fail and Discontinue', 'Fail and Discontinue'), ('Health Reasons', 'Health Reasons'), ('Fail and Exclude', 'Fail and Exclude'), ('Continuing Student', 'Continuing Student')], default='Fail and Discontinue', max_length=100)),
                ('semesters_passed', models.PositiveIntegerField(default=1)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_programme', to='accounts.Programme')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuProg_planCode', to='accounts.Programme')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentProg_studentID', to='accounts.Student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_grade', models.PositiveIntegerField(default=0)),
                ('GPA', models.DecimalField(decimal_places=2, max_digits=3)),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Course')),
                ('overall_semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StudentCourse_overall_semester', to='accounts.ProgramSemester')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StudentCourse_semester', to='accounts.Course')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCGPA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CGPA', models.DecimalField(decimal_places=2, max_digits=3)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='overall_semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_overallSem', to='accounts.ProgramSemester'),
        ),
    ]
