# Generated by Django 4.2.2 on 2023-06-29 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreBusinessHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=255)),
                ('day', models.PositiveIntegerField()),
                ('start_time_local', models.TimeField()),
                ('end_time_local', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StoreStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('timestamp_utc', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StoreTimezone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=255)),
                ('timezone_str', models.CharField(max_length=255)),
            ],
        ),
    ]
