# Generated by Django 4.2.14 on 2024-08-19 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='uploaded_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
