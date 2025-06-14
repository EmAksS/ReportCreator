# Generated by Django 5.1.6 on 2025-05-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0027_template_persons_name_combination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfield',
            name='name',
            field=models.TextField(max_length=50, verbose_name='Русское название поля (для отображения)'),
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.TextField(max_length=50, verbose_name='Русское название поля (для отображения)'),
        ),
        migrations.AlterField(
            model_name='tablefield',
            name='name',
            field=models.TextField(max_length=50, verbose_name='Русское название поля (для отображения)'),
        ),
    ]
