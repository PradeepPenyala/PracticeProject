# Generated by Django 4.2.11 on 2024-04-05 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_remove_blogpost_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='like',
            field=models.TextField(blank=True, default=0, max_length=10, null=True),
        ),
    ]