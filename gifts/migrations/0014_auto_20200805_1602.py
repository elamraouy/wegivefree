# Generated by Django 3.0.8 on 2020-08-05 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0013_auto_20200805_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftrequest',
            name='gift',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='giftrequest',
            name='owner',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='giftrequest',
            name='user',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
