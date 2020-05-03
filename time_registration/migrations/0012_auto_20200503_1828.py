# Generated by Django 3.0.5 on 2020-05-03 16:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('time_registration', '0011_auto_20200501_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brake',
            name='added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='timeregistration',
            name='brakes',
            field=models.ManyToManyField(blank=True, to='time_registration.Brake'),
        ),
        migrations.AlterField(
            model_name='timeregistration',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
