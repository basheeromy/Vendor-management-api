# Generated by Django 4.2.7 on 2023-11-24 12:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(max_length=100, unique=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('out-to-deliver', 'Out-to-deliver'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=30)),
                ('quality_rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('issue_date', models.DateTimeField(null=True)),
                ('acknowledgment_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
