# Generated by Django 3.0.8 on 2021-03-22 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Minimaliste', '0005_post_pays'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='price',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]