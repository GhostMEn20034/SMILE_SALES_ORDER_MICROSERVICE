# Generated by Django 5.0.6 on 2024-06-18 14:09

import django.db.models.deletion
import django.db.models.expressions
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0002_alter_address_user'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processed', 'Processed'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='addresses.address', to_field='original_id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='original_id')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=13)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('amount', models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(models.F('price_per_unit'), '*', models.F('quantity')), output_field=models.DecimalField(decimal_places=2, max_digits=13))),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', to_field='order_uuid')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', to_field='object_id')),
            ],
        ),
    ]
