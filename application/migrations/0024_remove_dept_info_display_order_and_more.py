# Generated by Django 5.1.3 on 2025-01-14 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0023_alter_scientific_staff_alt_email_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dept_info',
            name='display_order',
        ),
        migrations.RemoveField(
            model_name='dept_info',
            name='hod_id',
        ),
        migrations.RemoveField(
            model_name='dept_info',
            name='staff_display_order',
        ),
    ]
