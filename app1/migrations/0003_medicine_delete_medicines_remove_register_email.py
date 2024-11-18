# Generated by Django 5.1.2 on 2024-11-18 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_medicines_register_delete_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=30)),
                ('Medication', models.CharField(max_length=50)),
                ('Dosage', models.CharField(max_length=50)),
                ('frequency', models.CharField(max_length=35)),
                ('additional_notes', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='medicines',
        ),
        migrations.RemoveField(
            model_name='register',
            name='email',
        ),
    ]
