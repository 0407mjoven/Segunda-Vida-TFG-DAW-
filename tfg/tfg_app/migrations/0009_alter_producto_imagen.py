# Generated by Django 5.0.6 on 2024-05-18 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfg_app', '0008_comentario_create_datetime_alter_producto_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='productos'),
        ),
    ]
