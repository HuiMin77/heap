# Generated by Django 4.2.3 on 2023-08-06 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_cca_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="image_url",
        ),
        migrations.RemoveField(
            model_name="event",
            name="manager",
        ),
        migrations.AddField(
            model_name="event",
            name="attendees",
            field=models.ManyToManyField(blank=True, null=True, to="events.student"),
        ),
        migrations.AlterField(
            model_name="student",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="User Email"
            ),
        ),
    ]