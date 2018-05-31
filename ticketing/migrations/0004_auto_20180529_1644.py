# Generated by Django 2.0.5 on 2018-05-29 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_auto_20180529_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema_comment',
            name='score',
            field=models.FloatField(choices=[(0.0, '0'), (1.0, '1'), (2.0, '2'), (3.0, '3'), (4.0, '4'), (5.0, '5'), (6.0, '6'), (7.0, '7'), (8.0, '8'), (9.0, '9'), (10.0, '10')]),
        ),
        migrations.AlterField(
            model_name='movie_comment',
            name='score',
            field=models.FloatField(choices=[(0.0, '0'), (1.0, '1'), (2.0, '2'), (3.0, '3'), (4.0, '4'), (5.0, '5'), (6.0, '6'), (7.0, '7'), (8.0, '8'), (9.0, '9'), (10.0, '10')]),
        ),
    ]