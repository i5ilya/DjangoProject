# Generated by Django 4.1 on 2022-10-29 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servio', '0002_alter_servio_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='servio',
            name='token_valid',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]