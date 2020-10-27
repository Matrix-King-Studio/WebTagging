from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0009_auto_20180917_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='labeledbox',
            name='client_id',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='labeledpoints',
            name='client_id',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='labeledpolygon',
            name='client_id',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='labeledpolyline',
            name='client_id',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='objectpath',
            name='client_id',
            field=models.BigIntegerField(default=-1),
        ),
    ]
