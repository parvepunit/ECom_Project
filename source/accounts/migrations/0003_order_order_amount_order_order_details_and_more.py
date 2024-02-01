# Generated by Django 4.1.5 on 2023-02-16 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_amount',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_details',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]