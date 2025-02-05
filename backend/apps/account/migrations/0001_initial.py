# Generated by Django 5.1.5 on 2025-01-24 02:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("person", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
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
                ("identifier", models.CharField(max_length=6)),
                ("last_login", models.DateTimeField(auto_now=True)),
                ("overdraft_protection", models.BooleanField(default=True)),
                (
                    "overdraft_limit",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("balance", models.DecimalField(decimal_places=2, max_digits=14)),
                (
                    "account_holder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="person.person"
                    ),
                ),
            ],
        ),
    ]
