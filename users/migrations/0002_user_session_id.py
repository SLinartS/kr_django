# Generated by Django 4.1.7 on 2023-02-17 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='session_id',
            field=models.CharField(max_length=30, null=True),
        ),
    ]