# Generated by Django 3.1.5 on 2021-01-28 21:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('name', models.CharField(max_length=200, verbose_name='city name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('name', models.CharField(max_length=50, verbose_name='organization name')),
                ('desc', models.TextField(verbose_name='description')),
                ('tag', models.CharField(default='famous', max_length=20, verbose_name='organization tag')),
                ('category', models.CharField(choices=[('pxjg', 'training institution'), ('gr', 'person'), ('gx', 'university')], default='pxjg', max_length=10, verbose_name='organization category')),
                ('click_nums', models.IntegerField(default=0, verbose_name='number of hits')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='number of collects')),
                ('image', models.ImageField(upload_to='org/%Y/%m', verbose_name='logo')),
                ('address', models.CharField(max_length=150, verbose_name='organization address')),
                ('students', models.IntegerField(default=0, verbose_name='number of students')),
                ('course_nums', models.IntegerField(default=0, verbose_name='number of courses')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.city', verbose_name='city')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('name', models.CharField(max_length=50, verbose_name='teacher name')),
                ('work_years', models.IntegerField(default=0, verbose_name='working years')),
                ('work_company', models.CharField(max_length=50, verbose_name='working company')),
                ('work_position', models.CharField(max_length=50, verbose_name='working position')),
                ('points', models.CharField(max_length=50, verbose_name='teaching specialties')),
                ('click_nums', models.IntegerField(default=0, verbose_name='number of hits')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='number of collects')),
                ('age', models.IntegerField(default=18, verbose_name='age')),
                ('image', models.ImageField(upload_to='teacher/%Y/%m', verbose_name='avatar')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.courseorg', verbose_name='organization')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]