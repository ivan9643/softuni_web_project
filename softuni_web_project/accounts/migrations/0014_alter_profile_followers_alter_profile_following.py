# Generated by Django 4.0.3 on 2022-04-10 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_profile_followers_alter_profile_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='followers_profiles', to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='following_profiles', to='accounts.profile'),
        ),
    ]
