# Generated by Django 2.2 on 2021-02-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_is_classical'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='click_num',
            field=models.IntegerField(default=0, verbose_name='Number of Clicks'),
        ),
    ]
