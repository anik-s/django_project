# Generated by Django 3.0.3 on 2020-04-20 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0003_auto_20200409_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='acquisition',
            name='transaction_name',
            field=models.CharField(default='Default Transaction', max_length=500),
            preserve_default=False,
        ),
    ]
