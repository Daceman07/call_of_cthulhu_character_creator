# Generated by Django 3.2.3 on 2021-06-10 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('char', '0010_auto_20210607_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='skills',
            name='Piloting',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='APP',
            field=models.IntegerField(default=85),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='CON',
            field=models.IntegerField(default=60),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='DEX',
            field=models.IntegerField(default=65),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='EDU',
            field=models.IntegerField(default=65),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='INT',
            field=models.IntegerField(default=80),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='LUCK',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='POW',
            field=models.IntegerField(default=65),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='SIZ',
            field=models.IntegerField(default=55),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='STR',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='skills',
            name='Art_Craft_Chosen',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AlterField(
            model_name='skills',
            name='Other_Language_Chosen',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AlterField(
            model_name='skills',
            name='Science_chosen',
            field=models.CharField(default='none', max_length=50),
        ),
    ]
