# Generated by Django 4.2.5 on 2023-10-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='breathability',
            field=models.CharField(choices=[('Низька', 'default2'), ('Майже відсутня', 'default3'), ('Середня', 'default'), ('Висока', 'default1')], default='Середня', max_length=30, verbose_name='Повітропроникність'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='color_fastness',
            field=models.CharField(choices=[('Висока стійкість', 'default'), ('Середня стійкість', 'default1'), ('Низька стійкість', 'default2'), ('Спеціалізована стійкість', 'default3'), ('Фарбована', 'default4'), ('Невідомо', 'default5')], default='Висока стійкість', max_length=30, verbose_name='Стійкість кольору'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='compression_resistance',
            field=models.CharField(choices=[('Висока стійкість', 'default'), ('Середня стійкість', 'default1'), ('Низька стійкість', 'default2'), ('Антикомпресійна тканина', 'default3')], default='Висока стійкість', max_length=30, verbose_name='Стійкість до стиснення'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='destiny',
            field=models.CharField(choices=[('Висока', 'default'), ('Помірна', 'default1'), ('Середня', 'default2'), ('Низька', 'default3'), ('Різна', 'default5')], default='Висока', max_length=30, verbose_name='Щільність'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='elasticity',
            field=models.CharField(choices=[('Не еластична', 'default'), ('Майже не еластична', 'default1'), ('Частоково еластична', 'default2'), ('Добре еластична', 'default3')], default='Не еластична', max_length=30, verbose_name='Еластичність'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='surface_texture',
            field=models.CharField(choices=[('Блискуча', 'default'), ('Геометрична', 'default1'), ('Гладка', 'default2'), ('Гофрована', 'default3'), ('Діагональна', 'default4'), ('Матова', 'default5'), ('Рельєфна', 'default6'), ('Рубчаста', 'default7'), ('Сітчаста', 'default8'), ('Складна', 'default9'), ('Смужкова', 'default10'), ('Шорстка', 'default11')], default='Блискуча', max_length=30, verbose_name='Текстура'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(max_length=50, verbose_name='Адреса(місто)'),
        ),
    ]
