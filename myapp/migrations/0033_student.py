# Generated by Django 4.2.11 on 2024-04-16 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_alter_coupon_coupon_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('student_name', models.CharField(blank=True, max_length=100, null=True)),
                ('course_names', models.ManyToManyField(blank=True, to='myapp.course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]