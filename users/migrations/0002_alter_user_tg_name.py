# Generated by Django 5.0.7 on 2024-09-02 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="tg_name",
            field=models.CharField(
                default="@Duzzz13", max_length=50, verbose_name="Telegram username"
            ),
            preserve_default=False,
        ),
    ]
