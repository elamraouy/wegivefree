# Generated by Django 3.0.8 on 2020-08-10 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0031_auto_20200810_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='gift',
        ),
        migrations.AddField(
            model_name='conversation',
            name='guest_image',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='host_image',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]