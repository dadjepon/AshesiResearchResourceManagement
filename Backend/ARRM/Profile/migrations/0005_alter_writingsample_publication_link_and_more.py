# Generated by Django 4.2.7 on 2023-11-26 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_writingsample'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writingsample',
            name='publication_link',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='writingsample',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]