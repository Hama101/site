# Generated by Django 3.0.8 on 2021-04-25 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Minimaliste', '0033_auto_20210425_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sub_sub',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
