# Generated by Django 4.2.11 on 2024-04-11 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_blogpost_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='like',
            field=models.IntegerField(blank=True, default=0, editable=False, null=True),
        ),
    ]