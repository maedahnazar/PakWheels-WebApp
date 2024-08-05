# Generated by Django 4.2.14 on 2024-08-05 14:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_remove_feature_cars_remove_image_car_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 8, 5, 14, 11, 8, 177712, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='last_modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='location',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='ad',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ad',
            name='title',
            field=models.TextField(),
        ),
    ]
