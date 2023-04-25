# Generated by Django 4.2 on 2023-04-25 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_name_auction_listing_listing_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
