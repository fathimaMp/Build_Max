# Generated by Django 4.2.6 on 2023-11-11 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildapp', '0020_alter_worker_req_workstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor_req',
            name='Status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='contractor_req',
            name='servicestatus',
            field=models.BooleanField(default=False),
        ),
    ]