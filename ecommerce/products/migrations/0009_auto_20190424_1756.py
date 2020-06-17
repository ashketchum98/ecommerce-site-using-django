# Generated by Django 2.1.7 on 2019-04-24 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20180719_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('img', models.ImageField(blank=True, null=True, upload_to='product_imgs/')),
            ],
        ),
        migrations.DeleteModel(
            name='Clothe',
        ),
        migrations.DeleteModel(
            name='Electronic',
        ),
        migrations.DeleteModel(
            name='Furniture',
        ),
    ]
