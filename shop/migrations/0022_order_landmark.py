# Generated by Django 3.0.8 on 2020-08-18 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_auto_20200812_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='landmark',
            field=models.CharField(default='', max_length=500),
        ),
    ]
