from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personalization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startLocation', models.CharField(max_length=100, verbose_name='Počiatočný bod')),
                ('endLocation', models.CharField(max_length=20, verbose_name='Koncový bod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Používateľ')),
            ],
            options={
                'verbose_name': 'Obľúbená trasa',
                'verbose_name_plural': 'Obľúbené trasy',
                'unique_together': {('user', 'startLocation', 'endLocation')},
            },
        ),
        migrations.DeleteModel(
            name='FavoriteRoute',
        ),
    ]