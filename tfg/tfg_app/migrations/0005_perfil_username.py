# Generated by Django 5.0.6 on 2024-06-06 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfg_app', '0004_perfil_customer_id_producto_price_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='username',
            field=models.CharField(default='a', max_length=200),
            preserve_default=False,
        ),
    ]