# Generated by Django 3.0.8 on 2020-08-15 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0040_auto_20200812_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='request',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='gifts.GiftRequest'),
        ),
    ]
