# Generated by Django 4.2.5 on 2023-10-18 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_customer_email_alter_fabric_breathability_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='receipt',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.receipt'),
        ),
    ]
