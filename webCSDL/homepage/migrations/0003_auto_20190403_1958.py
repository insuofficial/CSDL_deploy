# Generated by Django 2.1.7 on 2019-04-03 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20190403_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patent',
            name='id',
            field=models.IntegerField(max_length=255, primary_key=True, serialize=False),
        ),
    ]