import cvat.apps.auto_annotation.models
from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', cvat.apps.auto_annotation.models.SafeCharField(max_length=256)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('model_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(),
                                                upload_to=cvat.apps.auto_annotation.models.upload_path_handler)),
                ('weights_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(),
                                                  upload_to=cvat.apps.auto_annotation.models.upload_path_handler)),
                ('labelmap_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(),
                                                   upload_to=cvat.apps.auto_annotation.models.upload_path_handler)),
                ('interpretation_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(),
                                                         upload_to=cvat.apps.auto_annotation.models.upload_path_handler)),
                ('shared', models.BooleanField(default=False)),
                ('primary', models.BooleanField(default=False)),
                ('framework',
                 models.CharField(default=cvat.apps.auto_annotation.models.FrameworkChoice('openvino'), max_length=32)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]
