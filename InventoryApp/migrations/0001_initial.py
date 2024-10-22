# Generated by Django 4.2.16 on 2024-10-22 08:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(max_length=255)),
                ('capacity', models.PositiveIntegerField()),
                ('current_inventory', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='KabupatenKota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('id_code', models.CharField(max_length=20, unique=True)),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Kecamatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('id_code', models.CharField(max_length=20, unique=True)),
                ('kabupaten_kota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kecamatan', to='InventoryApp.kabupatenkota')),
            ],
        ),
        migrations.CreateModel(
            name='KelurahanDesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('id_code', models.CharField(max_length=20, unique=True)),
                ('postal_code', models.CharField(max_length=10)),
                ('kecamatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelurahan_desa', to='InventoryApp.kecamatan')),
            ],
        ),
        migrations.CreateModel(
            name='Provinsi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('id_code', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('capacity', models.PositiveIntegerField()),
                ('manager', models.CharField(blank=True, max_length=255, null=True)),
                ('current_inventory', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('address_line1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Alamat Baris 1')),
                ('address_line2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Alamat Baris 2')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Alamat Email')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InventoryApp.kecamatan')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InventoryApp.provinsi')),
                ('regency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InventoryApp.kabupatenkota')),
                ('village', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InventoryApp.kelurahandesa')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('capacity', models.PositiveIntegerField()),
                ('current_inventory', models.PositiveIntegerField(default=0)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='InventoryApp.area')),
            ],
        ),
        migrations.AddField(
            model_name='kabupatenkota',
            name='provinsi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kabupaten_kota', to='InventoryApp.provinsi'),
        ),
        migrations.AddField(
            model_name='area',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='InventoryApp.warehouse'),
        ),
    ]
