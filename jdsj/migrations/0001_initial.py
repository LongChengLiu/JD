# Generated by Django 3.0.3 on 2020-04-08 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('skid', models.TextField()),
                ('color', models.TextField()),
                ('img_url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Phone_jdsj',
            fields=[
                ('pid', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('skid', models.TextField()),
                ('config', models.TextField()),
                ('price', models.FloatField()),
                ('color', models.TextField()),
                ('configs', models.TextField()),
                ('defaultGoodCount', models.IntegerField()),
                ('defaultGoodCountStr', models.TextField()),
                ('commentCount', models.IntegerField()),
                ('commentCountStr', models.TextField()),
                ('goodRateShow', models.FloatField()),
                ('title', models.TextField(default='1')),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('image_id', models.IntegerField(primary_key=True, serialize=False)),
                ('skid', models.IntegerField()),
                ('img_url', models.TextField()),
            ],
        ),
    ]