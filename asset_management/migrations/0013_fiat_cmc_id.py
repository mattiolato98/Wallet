# Generated by Django 3.1.7 on 2021-03-14 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_management', '0012_fiat'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiat',
            name='cmc_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
