# Generated by Django 4.1.5 on 2023-02-16 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('On Progress', 'On Progress'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Deliverd', 'Deliverd')], max_length=50)),
            ],
        ),
    ]
