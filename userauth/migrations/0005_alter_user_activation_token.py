# Generated by Django 5.1.6 on 2025-03-08 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0004_alter_user_activation_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_token',
            field=models.CharField(blank=True, default='RICiKRYPOv95Jbeqhp5HdhvtYZjSBmFB', max_length=100, null=True),
        ),
    ]
