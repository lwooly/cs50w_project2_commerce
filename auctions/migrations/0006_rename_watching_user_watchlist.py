# Generated by Django 4.2 on 2023-04-26 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_user_watching'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='watching',
            new_name='watchlist',
        ),
    ]
