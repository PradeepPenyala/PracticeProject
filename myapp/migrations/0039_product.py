# Generated by Django 4.2.11 on 2024-05-22 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0038_follow_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('product_type', models.CharField(blank=True, max_length=100, null=True)),
                ('product_price', models.IntegerField(default=0.0)),
                ('quality', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]