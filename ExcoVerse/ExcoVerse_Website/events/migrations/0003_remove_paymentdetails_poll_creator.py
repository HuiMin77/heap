# Generated by Django 4.2.3 on 2023-08-05 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_paymentpoll_poll_id_paymentpoll_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentdetails',
            name='poll_creator',
        ),
    ]
