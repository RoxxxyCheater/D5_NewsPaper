# Generated by Django 4.0.5 on 2022-07-20 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_subscribersmail_subscriber_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribersmail',
            name='href',
            field=models.TextField(default=''),
        ),
    ]
