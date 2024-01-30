# Generated by Django 5.0.1 on 2024-01-25 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("content", models.TextField()),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="post_image/"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("value", models.BooleanField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("object_id", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100)),
                ("content", models.TextField()),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
            ],
        ),
    ]
