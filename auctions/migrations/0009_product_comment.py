# Generated by Django 4.0.4 on 2022-07-25 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.comment'),
        ),
    ]
