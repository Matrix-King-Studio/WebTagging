from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0006_auto_20180629_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='flipped',
            field=models.BooleanField(default=False),
        ),
    ]
