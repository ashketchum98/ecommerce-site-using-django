# Generated by Django 2.0.1 on 2018-07-19 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20180719_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latestdeal',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]