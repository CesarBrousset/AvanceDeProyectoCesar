# Generated by Django 3.2.15 on 2022-10-08 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="articulo",
            old_name="cuerpo",
            new_name="texto",
        ),
        migrations.RenameField(
            model_name="comentario",
            old_name="cuerpo",
            new_name="comentario",
        ),
    ]
