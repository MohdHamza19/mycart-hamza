# Generated by Django 3.0.8 on 2020-08-26 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_auto_20200827_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=models.ImageField(blank=True, default='', upload_to='shop/images'),
        ),
    ]
