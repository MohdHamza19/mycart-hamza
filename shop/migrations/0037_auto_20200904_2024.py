# Generated by Django 3.0.8 on 2020-09-04 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0036_auto_20200904_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product2',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='product3',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='product4',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='product5',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='product6',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity2',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity3',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity4',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity5',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity6',
            field=models.CharField(default='', max_length=50),
        ),
    ]