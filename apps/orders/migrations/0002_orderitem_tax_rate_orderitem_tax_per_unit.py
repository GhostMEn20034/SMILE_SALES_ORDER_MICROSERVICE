# Generated by Django 5.0.6 on 2024-07-04 14:54

import django.core.validators
import django.db.models.expressions
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='tax_rate',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=3, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))]),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='tax_per_unit',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(models.F('price_per_unit'), '*', models.F('tax_rate')), output_field=models.DecimalField(decimal_places=2, max_digits=13)),
        ),
    ]
