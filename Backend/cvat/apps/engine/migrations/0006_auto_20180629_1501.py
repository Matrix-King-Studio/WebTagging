from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0005_auto_20180609_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='labeledbox',
            name='group_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='labeledpoints',
            name='group_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='labeledpolygon',
            name='group_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='labeledpolyline',
            name='group_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='objectpath',
            name='group_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
