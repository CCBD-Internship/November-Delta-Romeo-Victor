# Generated by Django 3.0.7 on 2020-07-07 16:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eval', '0010_auto_20200707_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Invalid Phone number', regex='^[0-9]{10}$')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Invalid Phone number', regex='^[0-9]{10}$')]),
        ),
    ]