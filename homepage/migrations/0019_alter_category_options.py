# Generated by Django 5.0.1 on 2024-02-03 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0018_alter_category_options_category_order"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ("order",)},
        ),
    ]
