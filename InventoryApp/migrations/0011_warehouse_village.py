# Generated by Django 4.2.15 on 2024-09-02 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryApp', '0010_village'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InventoryApp.village'),
        ),
    ]
