# Generated by Django 5.1.3 on 2025-02-06 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0082_alter_circular_list_circular_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertise_list',
            name='advertise_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tender_list',
            name='tender_date',
            field=models.DateField(null=True),
        ),
    ]
