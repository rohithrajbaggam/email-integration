# Generated by Django 4.0.5 on 2022-06-18 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_appemailusercredentialsmodel_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appemaildatamodel',
            name='dir',
            field=models.CharField(default='-', max_length=100),
        ),
    ]
