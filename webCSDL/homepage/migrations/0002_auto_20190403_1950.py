# Generated by Django 2.1.7 on 2019-04-03 10:50

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patent',
            name='location',
            field=models.CharField(choices=[('International Patent', 'International Patent'), ('Korean Patent', 'Korean Patent')], default='International Patent', max_length=128),
        ),
        migrations.AddField(
            model_name='patent',
            name='patent',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patent',
            name='year',
            field=models.IntegerField(choices=[(2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019),
        ),
    ]
