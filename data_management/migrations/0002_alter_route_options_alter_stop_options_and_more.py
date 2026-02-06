from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['name'], 'verbose_name': 'Linka', 'verbose_name_plural': 'Linky'},
        ),
        migrations.AlterModelOptions(
            name='stop',
            options={'ordering': ['name'], 'verbose_name': 'Zastávka', 'verbose_name_plural': 'Zastávky'},
        ),
        migrations.AlterModelOptions(
            name='trip',
            options={'ordering': ['departure_time'], 'verbose_name': 'Spoj', 'verbose_name_plural': 'Spoje'},
        ),
        migrations.AddField(
            model_name='route',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Vytvorená'),
        ),
        migrations.AddField(
            model_name='stop',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Vytvorená'),
        ),
        migrations.AddField(
            model_name='stop',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Aktualizovaná'),
        ),
        migrations.AddField(
            model_name='trip',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Vytvorený'),
        ),
        migrations.AlterField(
            model_name='route',
            name='end_stop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='routes_end', to='data_management.stop', verbose_name='Koncová zastávka'),
        ),
        migrations.AlterField(
            model_name='route',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Číslo/Názov linky'),
        ),
        migrations.AlterField(
            model_name='route',
            name='start_stop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='routes_start', to='data_management.stop', verbose_name='Začiatočná zastávka'),
        ),
        migrations.AlterField(
            model_name='stop',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Zemepisná šírka'),
        ),
        migrations.AlterField(
            model_name='stop',
            name='location',
            field=models.CharField(default='', max_length=200, verbose_name='Poloha'),
        ),
        migrations.AlterField(
            model_name='stop',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Zemepisná dĺžka'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='arrival_time',
            field=models.TimeField(verbose_name='Čas príchodu'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='departure_time',
            field=models.TimeField(verbose_name='Čas odchodu'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='vehicleID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.vehicle', verbose_name='Vozidlo'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='capacity',
            field=models.IntegerField(default=50, verbose_name='Kapacita'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='registration_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='ŠPZ'),
        ),
    ]