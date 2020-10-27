import cvat.apps.git.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('git', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitdata',
            name='status',
            field=models.CharField(default=cvat.apps.git.models.GitStatusChoice('!sync'), max_length=20),
        ),
    ]
