# Generated by Django 3.0.2 on 2020-01-07 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileShare_app', '0003_auto_20200106_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myfile',
            name='a_file',
            field=models.CharField(max_length=255),
        ),
    ]
