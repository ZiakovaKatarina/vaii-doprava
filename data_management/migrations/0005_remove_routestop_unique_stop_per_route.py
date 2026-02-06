from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0004_alter_routestop_options_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='routestop',
            name='unique_stop_per_route',
        ),
    ]