# Generated by Django 2.0.1 on 2018-07-15 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile_no',
            field=models.IntegerField(),
        ),
    ]