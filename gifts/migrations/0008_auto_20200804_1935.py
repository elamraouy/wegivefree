# Generated by Django 3.0.8 on 2020-08-04 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0007_auto_20200804_1933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demandesgift',
            old_name='gift_id',
            new_name='gift',
        ),
        migrations.RenameField(
            model_name='demandesgift',
            old_name='user_id',
            new_name='user',
        ),
    ]