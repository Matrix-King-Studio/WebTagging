from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0020_remove_task_flipped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='frame_filter',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
