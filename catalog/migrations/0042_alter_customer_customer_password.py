# Generated by Django 4.2.5 on 2023-11-22 10:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0041_rename_address_customer_customer_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_password',
            field=models.CharField(max_length=40, validators=[django.core.validators.RegexValidator(code='invalid_password', message='Мінімум вісім символів,\n одна літера,\n одна цифра\n один спеціальний символ:', regex='^\\+380 \\d{2}-\\d{3}-\\d{2}-\\d{2}$')], verbose_name='Пароль'),
        ),
    ]
