# Generated by Django 3.0.6 on 2020-07-05 12:53

import Gallery.models
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=32)),
                ('country', models.CharField(max_length=64)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_code', models.CharField(max_length=2)),
                ('state_name', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['-state_name'],
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('homepage', models.URLField()),
                ('phone_number', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('project_date', models.DateField()),
                ('status', models.IntegerField(choices=[(0, 'Unspecified'), (1, 'Cancelled'), (2, 'Forthcoming'), (3, 'Postponed indefinitely'), (4, 'Active'), (5, 'Inactive'), (6, 'Unknown'), (7, 'deleted')], default=0)),
                ('h_first_floor_sq_ft', models.FloatField(default=0)),
                ('h_second_floor_sq_ft', models.FloatField(default=0)),
                ('h_bedrooms', models.FloatField(default=0)),
                ('h_baths', models.FloatField(default=0)),
                ('h_stories', models.IntegerField(default=0)),
                ('h_roof_pitch', models.CharField(max_length=8)),
                ('h_roof_system', models.CharField(max_length=16)),
                ('h_price', models.FloatField(default=0)),
                ('description', ckeditor.fields.RichTextField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gallery.City')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gallery.Provider')),
            ],
            options={
                'ordering': ['-project_date'],
            },
        ),
        migrations.CreateModel(
            name='HomeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=Gallery.models.get_image_location, verbose_name='Image')),
                ('date_taken', models.DateField(blank=True, editable=False)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Unspecified'), (1, 'Cancelled'), (2, 'Forthcoming'), (3, 'Postponed indefinitely'), (4, 'Active'), (5, 'Inactive'), (6, 'Unknown'), (7, 'deleted')], default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gallery.Project')),
            ],
            options={
                'ordering': ['-date_taken'],
            },
        ),
        migrations.AddField(
            model_name='city',
            name='id_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gallery.Location'),
        ),
    ]
