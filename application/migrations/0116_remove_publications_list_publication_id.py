# Generated by Django 5.1.3 on 2025-03-26 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0115_publications_list_publication_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publications_list',
            name='publication_id',
        ),
    ]
