# Generated by Django 4.2.11 on 2024-04-04 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_userotp_blogpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
    ]
