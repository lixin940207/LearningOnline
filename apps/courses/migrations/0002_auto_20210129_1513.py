# Generated by Django 2.2 on 2021-01-29 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={},
        ),
        migrations.RenameField(
            model_name='course',
            old_name='add_time',
            new_name='created_time',
        ),
        migrations.RenameField(
            model_name='courseresource',
            old_name='add_time',
            new_name='created_time',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='add_time',
            new_name='created_time',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='add_time',
            new_name='created_time',
        ),
    ]
