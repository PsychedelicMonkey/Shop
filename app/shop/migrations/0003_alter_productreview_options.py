# Generated by Django 4.2.2 on 2023-06-23 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_productreview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ('-created_at',)},
        ),
    ]
