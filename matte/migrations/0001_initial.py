# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 13:22
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.crypto


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SelectControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('controls', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Storyboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=django.utils.crypto.get_random_string, max_length=20, unique=True)),
                ('url', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('template_type', models.CharField(choices=[('Basic', 'Basic'), ('Compact', 'Compact'), ('fire_skin', 'fire_skin'), ('earth_skin', 'earth_skin'), ('forest_skin', 'forest_skin')], default='Basic', max_length=15)),
                ('extra_emails', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('raw_query', models.TextField(blank=True, null=True)),
                ('uuid', models.CharField(default=django.utils.crypto.get_random_string, max_length=20, unique=True)),
                ('chart_type', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('controls', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='matte.SelectControl')),
            ],
        ),
        migrations.AddField(
            model_name='storyboard',
            name='saved_charts',
            field=models.ManyToManyField(to='matte.Visualization'),
        ),
    ]
