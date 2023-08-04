# Generated by Django 4.2.3 on 2023-08-04 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('events', '0004_paymentdetails_alter_student_chat_id_paymentpoll'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentpoll',
            name='stripe_account_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='members.userprofile'),
        ),
    ]
