# Generated by Django 5.1.4 on 2024-12-26 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_site', '0002_userprofile_age_userprofile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='story_video',
            field=models.FileField(upload_to='story_video/'),
        ),
    ]
