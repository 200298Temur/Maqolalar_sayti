# Generated by Django 5.0.6 on 2024-06-10 08:31

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Katigoriya')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Muharir')),
            ],
            options={
                'verbose_name': 'Katigoriya',
                'verbose_name_plural': 'Katigoriya',
            },
        ),
        migrations.CreateModel(
            name='Maqola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(3, message='Min simvol 3'), django.core.validators.MaxLengthValidator(100, message='Max simvol 100')], verbose_name='Slug')),
                ('content', models.TextField(verbose_name='Content')),
                ('is_published', models.BooleanField(default=0, verbose_name='Ruxsat')),
                ('rejection', models.BooleanField(default=False, verbose_name='Rad etish')),
                ('message', models.TextField(null=True, verbose_name='Message')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='core.category', verbose_name='Katigoriya')),
            ],
            options={
                'verbose_name': 'Maqola',
                'verbose_name_plural': 'Maqolalar',
                'ordering': ['-time_create'],
                'indexes': [models.Index(fields=['-time_create'], name='core_maqola_time_cr_671618_idx')],
            },
        ),
    ]
