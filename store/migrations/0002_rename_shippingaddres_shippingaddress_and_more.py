# Generated by Django 4.0.2 on 2022-05-25 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShippingAddres',
            new_name='ShippingAddress',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='date_orderd',
            new_name='date_ordered',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='quntity',
            new_name='quantity',
        ),
    ]
