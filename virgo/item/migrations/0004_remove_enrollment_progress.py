# Generated by Django 4.1.13 on 2024-09-08 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0003_enrollment_is_completed_enrollment_progress"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="enrollment",
            name="progress",
        ),
    ]
