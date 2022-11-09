# Generated by Django 4.0.5 on 2022-06-18 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_appemaildatamodel_dir'),
    ]

    operations = [
        migrations.CreateModel(
            name='appGmailDirModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('dir', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]