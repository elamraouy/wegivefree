# Generated by Django 3.0.8 on 2020-07-29 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DemandesGift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('user_id', models.CharField(max_length=1452)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=50)),
                ('receiver', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Mygifts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domaine', models.CharField(choices=[('Vêtements', 'Vêtements'), ('Cours en photos', 'Cours en photos'), ('Education et enseigement', 'Education et enseigement'), ('Services sociaux', 'Services sociaux'), ('Services medicaux', 'Services medicaux')], max_length=55)),
                ('title', models.CharField(max_length=250)),
                ('body', models.TextField(max_length=2500)),
                ('image', models.ImageField(default='', upload_to='static/pics')),
                ('image_url', models.CharField(max_length=2083)),
                ('date_add', models.DateTimeField(auto_now=True)),
                ('is_given', models.CharField(default='no', max_length=3)),
            ],
            options={
                'ordering': ['-date_add'],
            },
        ),
    ]
