# Generated by Django 3.1.7 on 2021-03-13 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_management', '0010_auto_20210312_1755'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userasset',
            options={},
        ),
        migrations.RemoveField(
            model_name='userasset',
            name='amount',
        ),
    ]
