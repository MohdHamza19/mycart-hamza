# Generated by Django 3.0.8 on 2020-09-04 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_currentuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
