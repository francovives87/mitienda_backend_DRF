# Generated by Django 4.1.7 on 2023-05-16 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userpersonaldata_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_visitor', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
