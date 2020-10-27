from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('git', '0002_auto_20190123_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitdata',
            name='lfs',
            field=models.BooleanField(default=True),
        ),
    ]
