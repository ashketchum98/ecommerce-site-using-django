# Generated by Django 2.1.7 on 2019-04-24 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('ER', 'Electronics'), ('CL', 'Clothes'), ('FR', 'Furniture')], max_length=2),
        ),
    ]
