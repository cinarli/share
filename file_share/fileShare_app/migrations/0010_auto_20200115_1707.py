# Generated by Django 3.0.2 on 2020-01-15 13:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fileShare_app', '0009_myfile_can_see'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfile',
            name='publish',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='myfile',
            name='can_see',
            field=models.ManyToManyField(related_name='file', to=settings.AUTH_USER_MODEL),
        ),
    ]
