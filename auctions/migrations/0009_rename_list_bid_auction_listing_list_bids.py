# Generated by Django 4.2 on 2023-04-27 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auction_listing_list_bid_alter_user_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_listing',
            old_name='list_bid',
            new_name='list_bids',
        ),
    ]