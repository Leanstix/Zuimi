# Generated by Django 5.1.6 on 2025-03-10 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0006_alter_user_activation_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_token',
            field=models.CharField(blank=True, default='gfNzFUDF3xuY0HOCcmzaKBN1Z2Med04B', max_length=100, null=True),
        ),
    ]
