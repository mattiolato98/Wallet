# Generated by Django 3.1.7 on 2021-03-09 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_management', '0007_auto_20210309_1140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userasset',
            options={'ordering': ['-quantity']},
        ),
    ]
