# Generated by Django 4.2.7 on 2023-11-29 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_rename_create_at_vendorperformance_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorperformance',
            name='po_deli_on_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vendorperformance',
            name='po_delivered',
            field=models.IntegerField(default=0),
        ),
    ]
