# Generated by Django 5.1.3 on 2025-01-17 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0037_rename_category_staff_designation_category_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projects',
            old_name='department_name',
            new_name='category_name',
        ),
    ]
