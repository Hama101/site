# Generated by Django 3.0.8 on 2021-03-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Minimaliste', '0003_auto_20210319_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, choices=[('Marketplace', 'Marketplace'), ('Location', 'Location'), ('Services', 'Services'), ('Echange', 'Echange'), ('Object gratuits', 'Object gratuits')], max_length=30, null=True),
        ),
    ]
