# Generated by Django 2.1.7 on 2019-06-11 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_auto_20190607_1637'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
    ]