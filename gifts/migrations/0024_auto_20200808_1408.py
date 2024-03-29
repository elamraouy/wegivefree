# Generated by Django 3.0.8 on 2020-08-08 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gifts', '0023_delete_giftstatistiques'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messages',
            options={'ordering': ['-date_send']},
        ),
        migrations.RemoveField(
            model_name='messages',
            name='receiver',
        ),
        migrations.AddField(
            model_name='messages',
            name='date_read',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='messages',
            name='date_send',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='messages',
            name='gift',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='gifts.Mygifts'),
        ),
        migrations.AddField(
            model_name='messages',
            name='viewd',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='messages',
            name='message',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
