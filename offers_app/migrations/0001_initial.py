# Generated by Django 5.1.3 on 2024-11-22 17:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.FileField(blank=True, null=True, upload_to='offers/')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('min_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('min_delivery_time', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OfferDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_type', models.CharField(choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('revisions', models.IntegerField()),
                ('delivery_time_in_days', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('features', models.JSONField()),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='offers_app.offer')),
            ],
            options={
                'ordering': ['offer_type'],
            },
        ),
    ]