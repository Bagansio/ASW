# Generated by Django 3.2.12 on 2022-04-24 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='comments',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
