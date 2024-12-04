# Generated by Django 5.1.3 on 2024-12-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='offer_type',
            field=models.CharField(choices=[('basic', 'Basic'), ('premium', 'Premium'), ('standard', 'Standard')], default='basic', max_length=20),
        ),
    ]