# Generated by Django 2.1.2 on 2018-10-16 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biller_app', '0002_auto_20181016_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callendrecord',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
