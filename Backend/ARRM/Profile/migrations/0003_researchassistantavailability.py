# Generated by Django 4.2.7 on 2023-12-10 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Miscelleneous', '0001_initial'),
        ('Profile', '0002_alter_interest_study_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchAssistantAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profile.researchassistant')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Miscelleneous.semester')),
            ],
        ),
    ]
