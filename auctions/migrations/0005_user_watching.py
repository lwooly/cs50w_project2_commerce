# Generated by Django 4.2 on 2023-04-26 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auction_listing_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watching',
            field=models.ManyToManyField(blank=True, related_name='watcher', to='auctions.auction_listing'),
        ),
    ]