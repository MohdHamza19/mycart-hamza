# Generated by Django 3.0.8 on 2020-09-04 14:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_auto_20200904_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
