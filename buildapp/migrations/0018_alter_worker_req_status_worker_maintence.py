# Generated by Django 4.2.6 on 2023-11-08 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildapp', '0017_contractor_req_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker_req',
            name='Status',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='worker_maintence',
            fields=[
                ('MaintenanceId', models.AutoField(primary_key=True, serialize=False)),
                ('worker_maintenance_image', models.ImageField(blank=True, null=True, upload_to='worker_maintenance/')),
                ('Status', models.BooleanField(default=True)),
                ('ReqId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildapp.worker_req')),
            ],
        ),
    ]