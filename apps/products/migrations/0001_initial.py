# Generated by Django 5.0.6 on 2024-06-05 20:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, unique=True)),
                ('parent_id', models.CharField(blank=True, db_index=True, null=True)),
                ('name', models.CharField()),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=13)),
                ('discount_rate', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('tax_rate', models.DecimalField(db_index=True, decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('stock', models.PositiveIntegerField(default=0)),
                ('max_order_qty', models.PositiveIntegerField(default=0)),
                ('sku', models.CharField()),
                ('for_sale', models.BooleanField(db_index=True, default=True)),
                ('image', models.URLField()),
                ('event_id', models.CharField(blank=True, db_index=True, default=None, null=True)),
            ],
        ),
    ]
