# Generated by Django 5.1.3 on 2024-12-27 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_rename_department_name_department_staff_hod_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='dept_info',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
