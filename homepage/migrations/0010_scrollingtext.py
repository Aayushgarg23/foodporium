# Generated by Django 5.0.1 on 2024-01-27 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0009_menuitem_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScrollingText",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
            ],
        ),
    ]
