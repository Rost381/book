# Generated by Django 3.0.5 on 2021-01-21 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='autor_name',
            field=models.CharField(default='autor', max_length=255),
            preserve_default=False,
        ),
    ]
