# Generated by Django 5.1.4 on 2024-12-11 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_following_like'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Following',
            new_name='Follow',
        ),
    ]