# Generated by Django 3.0.8 on 2020-08-12 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20200812_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='revid',
        ),
    ]
