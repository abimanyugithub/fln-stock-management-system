# Generated by Django 4.2.16 on 2024-10-22 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='capacity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
