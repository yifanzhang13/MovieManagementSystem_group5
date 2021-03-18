# Generated by Django 3.1.7 on 2021-03-17 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='movies',
            fields=[
                ('MovieID', models.IntegerField(primary_key=True, serialize=False)),
                ('MovieTitle', models.CharField(max_length=255)),
                ('MovieGenres', models.CharField(max_length=255)),
            ],
        ),
    ]
