# Generated by Django 4.0.1 on 2022-01-31 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_cv_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
