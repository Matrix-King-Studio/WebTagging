from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0003_objectpath_shapes'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='z_order',
            field=models.BooleanField(default=False),
        ),
    ]
