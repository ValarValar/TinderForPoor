# Generated by Django 3.2.7 on 2021-11-30 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientsApp', '0004_alter_user_liked_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked_list',
            field=models.JSONField(blank=True, default=list),
        ),
    ]