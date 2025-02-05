# Generated by Django 5.1.5 on 2025-01-24 02:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Continent",
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
            name="Country",
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
                ("code", models.CharField(max_length=2, unique=True)),
                (
                    "continent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="location.continent",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="City",
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
                (
                    "type",
                    models.CharField(
                        choices=[("C", "City"), ("T", "Town")],
                        default="C",
                        max_length=1,
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="location.country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Neighborhood",
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
                (
                    "type",
                    models.CharField(
                        choices=[("N", "Neighborhood"), ("C", "Community")],
                        default="N",
                        max_length=1,
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="location.city"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="State",
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
                (
                    "type",
                    models.CharField(
                        choices=[("S", "State"), ("P", "Province")],
                        default="S",
                        max_length=1,
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="location.country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="County",
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
                (
                    "type",
                    models.CharField(
                        choices=[("C", "County"), ("D", "District")],
                        default="C",
                        max_length=1,
                    ),
                ),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="location.state"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Street",
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
                ("postal_code", models.TextField()),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="location.city"
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="location.neighborhood",
                    ),
                ),
            ],
        ),
    ]
