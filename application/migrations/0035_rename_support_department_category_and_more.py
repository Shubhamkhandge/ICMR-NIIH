# Generated by Django 5.1.3 on 2025-01-16 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0034_projects_project_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='support_department',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='department_id',
            new_name='category_id',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='department_name',
            new_name='category_name',
        ),
    ]
