# Generated by Django 5.0.6 on 2024-07-22 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_returned_at_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_abandoned',
            field=models.BooleanField(default=False),
        ),
    ]
