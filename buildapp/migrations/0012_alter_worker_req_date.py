# Generated by Django 4.2.6 on 2023-10-28 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildapp', '0011_remove_services_wage1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker_req',
            name='Date',
            field=models.DateField(auto_now_add=True),
        ),
    ]