# Generated by Django 3.1 on 2021-05-03 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='images',
            new_name='image',
        ),
    ]
