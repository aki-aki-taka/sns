# Generated by Django 3.0.4 on 2022-08-03 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=2000),
        ),
    ]
