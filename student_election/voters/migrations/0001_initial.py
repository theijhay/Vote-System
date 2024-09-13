# Generated by Django 5.1.1 on 2024-09-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StudentVoter",
            fields=[
                (
                    "student_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("department", models.CharField(max_length=100)),
                ("year", models.IntegerField()),
                ("is_eligible", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]