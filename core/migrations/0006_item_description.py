# Generated by Django 3.2 on 2021-04-29 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_order_date_order_ordered_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='des', max_length=500),
            preserve_default=False,
        ),
    ]
