# Generated by Django 5.1.3 on 2025-03-21 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0114_remove_publications_list_publication_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='publications_list',
            name='publication_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
