# Generated by Django 3.2.12 on 2022-05-11 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_submission_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='votes',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]
