# Generated by Django 4.2 on 2023-04-27 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_list_bid_auction_listing_list_bids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction_listing',
            name='list_bids',
        ),
    ]
