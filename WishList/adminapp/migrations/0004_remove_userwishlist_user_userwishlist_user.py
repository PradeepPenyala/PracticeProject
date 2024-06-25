# Generated by Django 4.2.10 on 2024-02-28 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_remove_product_user_userwishlist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userwishlist',
            name='user',
        ),
        migrations.AddField(
            model_name='userwishlist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
