# Generated by Django 5.1.3 on 2025-02-04 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0068_project_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_staff',
            name='profile_status',
            field=models.BooleanField(default=True),
        ),
    ]
