# Generated by Django 4.2.16 on 2024-11-22 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_user_deposit_period_user_saving_period'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='nickname',
        ),
    ]
