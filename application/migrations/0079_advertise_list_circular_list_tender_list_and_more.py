# Generated by Django 5.1.3 on 2025-02-05 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0078_rename_alumini_join_year_alumini_staff_alumini_leave_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='advertise_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertise_id', models.CharField(max_length=255, null=True)),
                ('advertise_title', models.CharField(max_length=255, null=True)),
                ('advertise_date', models.DateTimeField(null=True)),
                ('advertise_file_name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='circular_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circular_id', models.CharField(max_length=255, null=True)),
                ('circular_title', models.CharField(max_length=255, null=True)),
                ('circular_date', models.DateTimeField(null=True)),
                ('circular_file_name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tender_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_id', models.CharField(max_length=255, null=True)),
                ('tender_title', models.CharField(max_length=255, null=True)),
                ('tender_date', models.DateTimeField(null=True)),
                ('tender_file_name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='advertise',
        ),
        migrations.DeleteModel(
            name='alumini',
        ),
    ]
