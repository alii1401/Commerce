# Generated by Django 4.0.4 on 2022-07-25 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_product_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='comment',
            new_name='comments',
        ),
    ]
