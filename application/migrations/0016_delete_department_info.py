# Generated by Django 5.1.3 on 2025-01-06 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_rename_department_department_info'),
    ]

    operations = [
        migrations.DeleteModel(
            name='department_info',
        ),
    ]
