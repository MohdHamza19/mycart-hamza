# Generated by Django 3.0.8 on 2020-08-08 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_orders_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
    ]
