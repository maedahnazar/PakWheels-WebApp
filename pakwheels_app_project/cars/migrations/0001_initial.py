# Generated by Django 4.2.14 on 2024-08-07 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_in', models.TextField()),
                ('color', models.TextField()),
                ('assembly', models.TextField()),
                ('engine_capacity', models.IntegerField()),
                ('body_type', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('ad', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='car', to='ads.ad')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InspectionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspected_date', models.DateField(blank=True, null=True)),
                ('overall_rating', models.TextField(blank=True, null=True)),
                ('grade', models.TextField(blank=True, null=True)),
                ('exterior_body', models.TextField(blank=True, null=True)),
                ('engine_transmission_clutch', models.TextField(blank=True, null=True)),
                ('suspension_steering', models.TextField(blank=True, null=True)),
                ('interior', models.TextField(blank=True, null=True)),
                ('ac_heater', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.car')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.source')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_image_url', models.URLField(blank=True, null=True)),
                ('uploaded_image', models.ImageField(blank=True, null=True, upload_to='car_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='cars.car')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('cars', models.ManyToManyField(related_name='features', to='cars.car')),
            ],
        ),
    ]
