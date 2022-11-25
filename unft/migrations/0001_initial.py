# Generated by Django 4.1.3 on 2022-11-25 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import unft.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Unft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_image', models.ImageField(max_length=255, upload_to=unft.models.upload_to_base)),
                ('style_image', models.ImageField(max_length=255, upload_to=unft.models.upload_to_style)),
                ('result_image', models.ImageField(max_length=255, upload_to=unft.models.upload_to_result)),
                ('title', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('hits', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_unft', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='own_unft', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'U-NFT',
                'verbose_name_plural': 'U-NFT',
                'db_table': 'U-NFT',
            },
        ),
    ]
