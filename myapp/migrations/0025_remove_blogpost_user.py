# Generated by Django 4.2.11 on 2024-04-11 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_blogpost_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='user',
        ),
    ]