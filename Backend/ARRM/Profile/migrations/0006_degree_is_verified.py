# Generated by Django 4.2.7 on 2023-11-27 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0005_alter_writingsample_publication_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='degree',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
