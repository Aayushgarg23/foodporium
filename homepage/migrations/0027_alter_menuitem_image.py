# Generated by Django 5.0.1 on 2024-02-05 05:06

import homepage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0026_alter_menuitem_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuitem",
            name="image",
            field=models.ImageField(
                upload_to="images/",
                validators=[homepage.models.validate_image_extension],
            ),
        ),
    ]