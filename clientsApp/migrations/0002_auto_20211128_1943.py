# Generated by Django 3.2.7 on 2021-11-28 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientsApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Sex',
            new_name='sex',
        ),
        migrations.AddField(
            model_name='user',
            name='liked_list',
            field=models.TextField(blank=True),
        ),
    ]