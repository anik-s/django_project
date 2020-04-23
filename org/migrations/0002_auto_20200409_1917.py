# Generated by Django 3.0.3 on 2020-04-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date_day',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='date_month',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='date_year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='thumbnail_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='url',
            field=models.URLField(null=True),
        ),
    ]