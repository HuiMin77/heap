# Generated by Django 4.2.3 on 2023-08-05 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_rename_manager_event_attendees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image_url',
        ),
    ]
