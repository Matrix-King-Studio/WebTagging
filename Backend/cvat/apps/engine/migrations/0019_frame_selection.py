from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0018_jobcommit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='start_frame',
        ),
        migrations.RemoveField(
            model_name='video',
            name='step',
        ),
        migrations.RemoveField(
            model_name='video',
            name='stop_frame',
        ),
        migrations.AddField(
            model_name='task',
            name='frame_filter',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='task',
            name='start_frame',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='stop_frame',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
