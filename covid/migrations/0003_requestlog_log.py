# Generated by Django 2.2.11 on 2020-04-13 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0002_requestlog_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestlog',
            name='log',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]