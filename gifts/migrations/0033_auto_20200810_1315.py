# Generated by Django 3.0.8 on 2020-08-10 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0032_auto_20200810_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='gift',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='gifts.Mygifts'),
        ),
    ]
