# Generated by Django 5.0.4 on 2024-04-07 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reffered_by',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
