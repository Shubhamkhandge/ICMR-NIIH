# Generated by Django 5.1.3 on 2025-01-27 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0050_rename_adminnistration_staff_administration_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='technical_staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tech_id', models.CharField(max_length=255, null=True)),
                ('tech_name', models.CharField(max_length=255, null=True)),
                ('support_department_name', models.CharField(max_length=255, null=True)),
                ('category_name', models.CharField(max_length=255, null=True)),
                ('designation', models.CharField(max_length=255, null=True)),
                ('email_id', models.CharField(max_length=200, null=True)),
                ('alt_email_id', models.CharField(max_length=200, null=True)),
                ('profilepic_name', models.CharField(max_length=255, null=True)),
                ('phone_no', models.CharField(max_length=255, null=True)),
                ('fax_no', models.CharField(max_length=255, null=True)),
                ('alt_phone_no', models.CharField(max_length=255, null=True)),
                ('level_no', models.CharField(max_length=255, null=True)),
                ('aadhar_no', models.CharField(max_length=255, null=True)),
                ('join_year', models.CharField(max_length=255, null=True)),
                ('author_name', models.CharField(max_length=255, null=True)),
                ('publications', models.TextField()),
                ('academic_background', models.TextField()),
                ('specialization', models.TextField()),
                ('professional_experience', models.TextField()),
                ('profile_status', models.CharField(max_length=255, null=True)),
                ('data_created', models.DateTimeField(null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='publication_copy',
            new_name='publications',
        ),
    ]
