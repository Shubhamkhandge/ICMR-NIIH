# Generated by Django 5.1.3 on 2025-01-24 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0047_support_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='support_department',
            old_name='sup_dept_id',
            new_name='support_department_id',
        ),
        migrations.RenameField(
            model_name='support_department',
            old_name='sup_dept_name',
            new_name='support_department_name',
        ),
        migrations.RenameField(
            model_name='support_department',
            old_name='sup_hod_name',
            new_name='support_hod_name',
        ),
    ]
