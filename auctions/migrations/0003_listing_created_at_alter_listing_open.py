# Generated by Django 5.0.3 on 2024-08-03 00:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing_comment_bid_user_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='listing',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]