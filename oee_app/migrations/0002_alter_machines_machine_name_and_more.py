# Generated by Django 5.0.4 on 2024-04-20 04:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oee_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machines',
            name='machine_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='machines',
            name='machine_serial_no',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='machines',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='cycle_no',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='duration',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oee_app.machines'),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='material_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='start_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='unique_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
