from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0004_task_z_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='labeledbox',
            name='z_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='labeledpoints',
            name='z_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='labeledpolygon',
            name='z_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='labeledpolyline',
            name='z_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trackedbox',
            name='z_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trackedpoints',
            name='z_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trackedpolygon',
            name='z_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trackedpolyline',
            name='z_order',
            field=models.IntegerField(default=0),
        ),
    ]
