# Generated by Django 5.0.7 on 2024-09-03 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_tg_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="tg_name",
            field=models.CharField(
                help_text="Введите Telegram User ID",
                max_length=50,
                verbose_name="Telegram username",
            ),
        ),
    ]
