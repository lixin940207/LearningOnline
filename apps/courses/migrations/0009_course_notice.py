# Generated by Django 2.2 on 2021-02-02 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_remove_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.CharField(default='', max_length=300, verbose_name='Course Notice'),
        ),
    ]
