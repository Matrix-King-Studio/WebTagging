from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0013_auth_no_default_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='max_shape_id',
            field=models.BigIntegerField(default=-1),
        ),
    ]
