# Generated by Django 3.0.8 on 2020-08-01 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0004_mygifts_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='mygifts',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/pics'),
        ),
        migrations.AlterField(
            model_name='mygifts',
            name='domaine',
            field=models.CharField(choices=[('Vêtements', 'Vêtements'), ('Aides budgétaires', 'Aides budgétaires'), ('Apprentissage des langues', 'Apprentissage des langues'), ('Cours en photos', 'Cours en photos'), ('Education et enseigement', 'Education et enseigement'), ('Services sociaux', 'Services sociaux'), ('Services medicaux', 'Services medicaux')], max_length=55),
        ),
        migrations.AlterField(
            model_name='mygifts',
            name='is_given',
            field=models.CharField(blank=True, default='no', max_length=3),
        ),
    ]
