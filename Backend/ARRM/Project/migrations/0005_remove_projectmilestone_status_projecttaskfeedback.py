# Generated by Django 4.2.7 on 2023-12-04 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Project', '0004_projectmilestone_projecttask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmilestone',
            name='status',
        ),
        migrations.CreateModel(
            name='ProjectTaskFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.projecttask')),
                ('target_ra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
