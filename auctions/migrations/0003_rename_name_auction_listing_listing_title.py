# Generated by Django 4.2 on 2023-04-25 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_listing',
            old_name='name',
            new_name='listing_title',
        ),
    ]