# Generated by Django 4.2.13 on 2024-07-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_builduniappfile_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsoninfo',
            name='tabbrs',
            field=models.TextField(blank=True, verbose_name='tabbars'),
        ),
    ]
