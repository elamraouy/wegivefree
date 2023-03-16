# Generated by Django 3.0.8 on 2020-08-04 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gifts', '0006_auto_20200803_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demandesgift',
            name='title',
        ),
        migrations.AddField(
            model_name='demandesgift',
            name='gift_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='gifts.Mygifts'),
        ),
        migrations.AddField(
            model_name='demandesgift',
            name='user_city',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='demandesgift',
            name='user_email',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='demandesgift',
            name='user_fb',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='demandesgift',
            name='user_message',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='demandesgift',
            name='user_name',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='demandesgift',
            name='user_phone',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='demandesgift',
            name='user_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mygifts',
            name='city',
            field=models.CharField(blank=True, choices=[('Safi', 'Safi'), ('Rabat', 'Rabat'), ('Agadir', 'Agadir'), ('Casablanca', 'Casablanca'), ('Marrakec', 'Marrakech'), ('Beni mellal', 'Beni mellal'), ('Oujda', 'Oujda'), ('Asilah', 'Asilah'), ('Tanger', 'Tanger'), ('Layoune', 'Layoune')], default='', max_length=55),
        ),
    ]