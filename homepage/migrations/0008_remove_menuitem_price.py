# Generated by Django 5.0.1 on 2024-01-24 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0007_category_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="menuitem",
            name="price",
        ),
    ]
