# Generated by Django 3.0.8 on 2021-04-25 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Minimaliste', '0032_blog_shortdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
