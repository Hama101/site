# Generated by Django 3.0.8 on 2021-04-26 13:40

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Minimaliste', '0035_auto_20210425_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=12, null=True), blank=True, null=True, size=None),
        ),
    ]
