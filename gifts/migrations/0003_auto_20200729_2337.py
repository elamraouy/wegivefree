# Generated by Django 3.0.8 on 2020-07-29 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0002_remove_mygifts_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='mygifts',
            name='user',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AddField(
            model_name='mygifts',
            name='user_id',
            field=models.CharField(default='', max_length=80),
        ),
    ]