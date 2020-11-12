from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0024_auto_20191023_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='chunk_size',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
