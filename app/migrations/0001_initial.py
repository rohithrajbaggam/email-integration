# Generated by Django 4.0.5 on 2022-06-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='appEmailDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smtp_id', models.CharField(max_length=100, unique=True)),
                ('from_user', models.EmailField(max_length=254)),
                ('to_user', models.EmailField(max_length=254)),
                ('cc_users', models.CharField(blank=True, max_length=1024, null=True)),
                ('subject', models.CharField(blank=True, max_length=1024, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('attachments', models.ImageField(blank=True, null=True, upload_to='attachments')),
                ('received_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]