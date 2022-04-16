# Generated by Django 4.0.3 on 2022-04-16 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.CharField(max_length=255)),
                ('gender', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'User',
                'managed': True,
            },
        ),
    ]
