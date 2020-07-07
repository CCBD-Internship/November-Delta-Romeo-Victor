# Generated by Django 3.0.7 on 2020-07-07 16:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eval', '0011_auto_20200707_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='srn',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='SRN incorrect', regex='^PES')]),
        ),
    ]
