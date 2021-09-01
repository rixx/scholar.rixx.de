# Generated by Django 3.2.6 on 2021-09-01 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tag",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="topic",
            name="slug",
        ),
        migrations.AlterField(
            model_name="topic",
            name="title",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]