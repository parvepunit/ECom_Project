# Generated by Django 4.1.5 on 2023-02-11 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_orders_alter_contact_phone_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calculation_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
                ('qty_persheet', models.IntegerField()),
                ('cst_persheet', models.IntegerField()),
            ],
        ),
    ]