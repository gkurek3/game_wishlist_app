# Generated by Django 3.1.1 on 2020-10-10 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_auto_20201010_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='game',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='wishlist.game'),
        ),
    ]