# Generated by Django 3.0.8 on 2021-04-24 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Minimaliste', '0024_post_shortdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]