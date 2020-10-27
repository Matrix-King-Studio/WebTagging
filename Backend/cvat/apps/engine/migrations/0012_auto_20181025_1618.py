import cvat.apps.engine.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0011_add_task_source_and_safecharfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(default=cvat.apps.engine.models.StatusChoice('annotation'), max_length=32),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default=cvat.apps.engine.models.StatusChoice('annotation'), max_length=32),
        ),
    ]
