# Generated by Django 5.0.6 on 2024-06-01 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfg_app', '0003_alter_perfil_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='customer_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='price_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='product_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]