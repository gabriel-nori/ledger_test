# Generated by Django 5.1.5 on 2025-01-24 02:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AddressType",
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
                ("name", models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Occupation",
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
                ("name", models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="StreetType",
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
                ("name", models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Person",
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
                ("name", models.TextField(max_length=100)),
                ("birthday", models.DateField(blank=True, null=True)),
                (
                    "sex",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("X", "Nonbinary")],
                        max_length=1,
                    ),
                ),
                (
                    "primary_email",
                    models.TextField(blank=True, max_length=320, null=True),
                ),
                ("document", models.TextField(max_length=50)),
                (
                    "occupation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="person.occupation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PersonAddress",
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
                ("street", models.TextField()),
                ("number", models.IntegerField()),
                ("complement", models.TextField(max_length=150)),
                (
                    "address_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="person.addresstype",
                    ),
                ),
                (
                    "street_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="person.streettype",
                    ),
                ),
            ],
        ),
    ]
