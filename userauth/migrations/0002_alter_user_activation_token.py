# Generated by Django 5.1.6 on 2025-02-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_token',
            field=models.CharField(default='ATocBqjxmAfVFyn15DcvIrfFNTuNTk4o', max_length=100),
        ),
    ]
