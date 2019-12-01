# Generated by Django 2.2.7 on 2019-11-28 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('username', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mID', models.PositiveIntegerField()),
                ('mName', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'manufacturers',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('numTrades', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name_plural': 'users',
            },
        ),
    ]
