# Generated by Django 4.2.13 on 2024-05-14 08:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mobile_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SCDHistory",
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
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("image", models.ImageField(upload_to="scd_images/")),
                ("diagnose", models.CharField(max_length=30)),
            ],
            options={
                "verbose_name": "SCD History",
                "verbose_name_plural": "SCD Histories",
            },
        ),
    ]