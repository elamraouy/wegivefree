# Generated by Django 3.0.8 on 2020-08-06 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0015_auto_20200806_1505'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='giftrequest',
            options={'ordering': ['-date_add']},
        ),
    ]
