# Generated by Django 3.1.7 on 2021-03-13 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20210301_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='public',
            field=models.BooleanField(default=1, verbose_name='公開状態'),
            preserve_default=False,
        ),
    ]