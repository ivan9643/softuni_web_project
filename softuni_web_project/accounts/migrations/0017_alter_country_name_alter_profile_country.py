# Generated by Django 4.0.3 on 2022-04-14 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_country_profile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.country'),
        ),
    ]
