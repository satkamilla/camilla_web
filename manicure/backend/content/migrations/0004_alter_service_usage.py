# Generated by Django 5.0.3 on 2024-06-03 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_alter_service_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='usage',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
