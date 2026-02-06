from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('personalization', '0002_favouriteroute_delete_favoriteroute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favouriteroute',
            name='endLocation',
            field=models.CharField(max_length=100, verbose_name='Koncový bod'),
        ),
    ]