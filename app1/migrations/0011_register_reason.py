# Generated by Django 5.1.2 on 2024-11-19 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_appointment_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='Reason',
            field=models.CharField(default='Sick', max_length=80),
        ),
    ]
