# Generated by Django 4.2 on 2024-01-23 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
