from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('engine', '0014_job_max_shape_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitData',
            fields=[
                ('task',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                      to='engine.Task')),
                ('url', models.URLField(max_length=2000)),
                ('path', models.CharField(max_length=256)),
                ('sync_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='!sync', max_length=20)),
            ],
        ),
    ]
