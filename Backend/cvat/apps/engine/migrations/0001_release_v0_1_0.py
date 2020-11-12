from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='LabeledBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame', models.PositiveIntegerField()),
                ('xtl', models.FloatField()),
                ('ytl', models.FloatField()),
                ('xbr', models.FloatField()),
                ('ybr', models.FloatField()),
                ('occluded', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Job')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Label')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LabeledBoxAttributeVal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.LabeledBox')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.AttributeSpec')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObjectPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame', models.PositiveIntegerField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Job')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Label')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObjectPathAttributeVal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.AttributeSpec')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.ObjectPath')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_frame', models.IntegerField()),
                ('stop_frame', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('size', models.PositiveIntegerField()),
                ('path', models.CharField(max_length=256)),
                ('mode', models.CharField(max_length=32)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='annotate', max_length=32)),
                ('bug_tracker', models.CharField(default='', max_length=2000)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                            to=settings.AUTH_USER_MODEL)),
                ('overlap', models.PositiveIntegerField(default=0)),
            ],
            options={
                'permissions': (
                ('view_task', 'Can see available tasks'), ('view_annotation', 'Can see annotation for the task'),
                ('change_annotation', 'Can modify annotation for the task')),
            },
        ),
        migrations.CreateModel(
            name='TrackedBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xtl', models.FloatField()),
                ('ytl', models.FloatField()),
                ('xbr', models.FloatField()),
                ('ybr', models.FloatField()),
                ('occluded', models.BooleanField(default=False)),
                ('frame', models.PositiveIntegerField()),
                ('outside', models.BooleanField(default=False)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.ObjectPath')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrackedBoxAttributeVal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.TrackedBox')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.AttributeSpec')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='segment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Task'),
        ),
        migrations.AddField(
            model_name='label',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Task'),
        ),
        migrations.AddField(
            model_name='job',
            name='segment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Segment'),
        ),
        migrations.AddField(
            model_name='attributespec',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Label'),
        ),
        migrations.AlterField(
            model_name='labeledbox',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='objectpath',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='trackedbox',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='labeledbox',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='objectpath',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='trackedbox',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='job',
            name='annotator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
