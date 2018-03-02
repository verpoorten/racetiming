# Generated by Django 2.0.2 on 2018-03-01 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(db_index=True, max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('gender', models.CharField(blank=True, choices=[('F', 'Féminin'), ('M', 'Masculin')], default=None, max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(db_index=True, max_length=150)),
                ('distance', models.DecimalField(decimal_places=2, max_digits=5)),
                ('unit', models.CharField(choices=[('KM', 'kilometers'), ('M', 'miles')], default='KM', max_length=30)),
                ('race_date', models.DateField()),
                ('race_start', models.TimeField(blank=True, null=True)),
                ('current', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateTimeField(blank=True, null=True)),
                ('attention', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Runner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(db_index=True, max_length=50)),
                ('first_name', models.CharField(db_index=True, max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('F', 'Féminin'), ('M', 'Masculin')], default=None, max_length=1, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('number', models.IntegerField(unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='timing.Category')),
                ('race', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='timing.Race')),
            ],
        ),
        migrations.AddField(
            model_name='ranking',
            name='runner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='timing.Runner'),
        ),
    ]
