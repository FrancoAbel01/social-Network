# Generated by Django 4.1.3 on 2023-02-21 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_comentario_postcom_alter_comentario_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='pais',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
