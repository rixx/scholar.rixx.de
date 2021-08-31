# Generated by Django 3.2.6 on 2021-08-31 21:00

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("text", models.TextField()),
                ("prediction_deadline", models.DateTimeField(null=True)),
                ("prediction_result", models.BooleanField(null=True)),
            ],
            options={
                "ordering": ("order",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=100)),
                ("url", models.URLField(null=True)),
                (
                    "trust",
                    models.IntegerField(
                        choices=[
                            (0, "incorrect"),
                            (1, "probably incorrect"),
                            (2, "who knows, 50/50 of being correct (pop sci)"),
                            (3, "better than 50/50 at least (good pop sci)"),
                            (4, "good source"),
                            (5, "excellent source"),
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=50)),
                ("slug", models.CharField(db_index=True, max_length=50, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=100)),
                ("slug", models.CharField(db_index=True, max_length=100, unique=True)),
                ("info_box", models.JSONField()),
                (
                    "language",
                    models.CharField(
                        choices=[("de", "German"), ("en", "English")],
                        default="en",
                        max_length=2,
                    ),
                ),
                ("tags", models.ManyToManyField(related_name="topics", to="core.Tag")),
                (
                    "translation",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="core.topic",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CardTopicThrough",
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
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.card"
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.topic"
                    ),
                ),
            ],
            options={
                "ordering": ("card", "topic"),
            },
        ),
        migrations.CreateModel(
            name="CardSourceThrough",
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
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.card"
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.source"
                    ),
                ),
            ],
            options={
                "ordering": ("card", "source"),
            },
        ),
        migrations.AddField(
            model_name="card",
            name="references",
            field=models.ManyToManyField(
                through="core.CardTopicThrough", to="core.Topic"
            ),
        ),
        migrations.AddField(
            model_name="card",
            name="sources",
            field=models.ManyToManyField(
                through="core.CardSourceThrough", to="core.Source"
            ),
        ),
        migrations.AddField(
            model_name="card",
            name="topic",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cards",
                to="core.topic",
            ),
        ),
    ]
