# Generated by Django 3.0.8 on 2020-08-10 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0033_auto_20200810_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='guest_image',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='host_image',
        ),
    ]