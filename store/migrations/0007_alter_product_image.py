# Generated by Django 4.0.6 on 2022-07-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0006_product_likes_delete_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photo/%Y/%m/%d/'),
        ),
    ]