# Generated by Django 3.2.3 on 2021-06-10 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('char', '0013_auto_20210610_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristics',
            name='APP',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='CON',
            field=models.IntegerField(default=55),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='DEX',
            field=models.IntegerField(default=45),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='EDU',
            field=models.IntegerField(default=85),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='LUCK',
            field=models.IntegerField(default=60),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='POW',
            field=models.IntegerField(default=45),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='SIZ',
            field=models.IntegerField(default=70),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='STR',
            field=models.IntegerField(default=30),
        ),
    ]