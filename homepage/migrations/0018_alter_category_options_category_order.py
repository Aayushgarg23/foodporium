# Generated by Django 5.0.1 on 2024-02-03 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0017_websiteorder_total"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["order"]},
        ),
        migrations.AddField(
            model_name="category",
            name="order",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
