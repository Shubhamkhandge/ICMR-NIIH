# Generated by Django 5.1.3 on 2025-01-29 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0056_bulletin_list_delete_bulletin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bulletin_list',
            name='bulletin_end_month',
        ),
        migrations.RemoveField(
            model_name='bulletin_list',
            name='bulletin_start_month',
        ),
    ]
