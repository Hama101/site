# Generated by Django 3.0.8 on 2021-03-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Minimaliste', '0004_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pays',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]