# Generated by Django 4.1.7 on 2023-03-23 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0015_remove_plan_blog_categories_remove_plan_blog_entries_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='images_x_services',
        ),
    ]
