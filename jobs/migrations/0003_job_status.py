# Generated by Django 4.2.16 on 2024-10-13 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_alter_job_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('stashed', 'Stashed')], default='active', max_length=10),
        ),
    ]
