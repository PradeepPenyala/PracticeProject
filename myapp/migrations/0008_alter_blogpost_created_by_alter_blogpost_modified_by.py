# Generated by Django 4.2.11 on 2024-04-04 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_blogpost_created_by_alter_blogpost_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='created_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='modified_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
