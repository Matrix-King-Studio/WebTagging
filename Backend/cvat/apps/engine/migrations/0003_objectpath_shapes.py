from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine',
         '0002_labeledpoints_labeledpointsattributeval_labeledpolygon_labeledpolygonattributeval_labeledpolyline_la'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectpath',
            name='shapes',
            field=models.CharField(default='boxes', max_length=10),
        ),
    ]
