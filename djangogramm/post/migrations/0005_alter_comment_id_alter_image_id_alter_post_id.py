# Generated by Django 5.0.1 on 2024-02-02 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0004_alter_tag_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]
