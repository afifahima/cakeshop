# Generated by Django 5.0.1 on 2024-01-10 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_wishlist_remove_payment_user_delete_orderplaced_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
