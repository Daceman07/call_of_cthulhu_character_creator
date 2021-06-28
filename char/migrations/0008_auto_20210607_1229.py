# Generated by Django 3.2.3 on 2021-06-07 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('char', '0007_auto_20210607_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backstory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cashandassets',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='APP',
            field=models.IntegerField(default=70),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='CON',
            field=models.IntegerField(default=70),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='EDU',
            field=models.IntegerField(default=70),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='INT',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='LUCK',
            field=models.IntegerField(default=45),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='POW',
            field=models.IntegerField(default=45),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='SIZ',
            field=models.IntegerField(default=45),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='STR',
            field=models.IntegerField(default=80),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='skills',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='weapons',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]