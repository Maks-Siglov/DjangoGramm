# Generated by Django 5.0.1 on 2024-02-02 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0003_alter_userprofile_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userprofile",
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
            },
        ),
    ]
