# Generated by Django 4.2.13 on 2024-06-19 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
    ]
