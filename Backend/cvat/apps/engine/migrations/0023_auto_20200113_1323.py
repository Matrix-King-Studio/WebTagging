import cvat.apps.engine.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0022_auto_20191004_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labeledimageattributeval',
            name='value',
            field=cvat.apps.engine.models.SafeCharField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='labeledshapeattributeval',
            name='value',
            field=cvat.apps.engine.models.SafeCharField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='labeledtrackattributeval',
            name='value',
            field=cvat.apps.engine.models.SafeCharField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='trackedshapeattributeval',
            name='value',
            field=cvat.apps.engine.models.SafeCharField(max_length=4096),
        ),
    ]
