# Generated by Django 4.2.3 on 2023-08-06 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CCA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='CCA Name')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Event Name')),
                ('start_event_date', models.DateTimeField(verbose_name='Event Start Date')),
                ('end_event_date', models.DateTimeField(verbose_name='Event End Date')),
                ('image_url', models.CharField(max_length=200, verbose_name='Event Image URL')),
                ('internal', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exco', models.BooleanField(default=False)),
                ('cca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.cca')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('student_id', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, verbose_name='User Email')),
                ('mobile_number', models.CharField(max_length=30)),
                ('chat_id', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Venue Name')),
                ('image_url', models.CharField(max_length=200, verbose_name='Venue Image URL')),
                ('address', models.CharField(max_length=300)),
                ('zip_code', models.CharField(max_length=15, verbose_name='Zip Code')),
                ('web', models.URLField(blank=True, verbose_name='Website Address')),
            ],
        ),
        migrations.CreateModel(
            name='Tracking_Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_success_excoverse', models.BooleanField(default=False)),
                ('is_success_club', models.BooleanField(default=False)),
                ('event', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.student')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=120, verbose_name='Subject')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Price')),
                ('password', models.CharField(max_length=6)),
                ('hashed_password', models.CharField(max_length=120)),
                ('payment_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('poll_creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('chat_id', models.IntegerField()),
                ('payment_id', models.CharField(max_length=255)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
                ('payment_provider', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.student')),
                ('poll_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.paymentpoll')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('membership', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.membership')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.student'),
        ),
        migrations.AddField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.student'),
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.venue'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField(default=False)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.student')),
            ],
        ),
    ]
