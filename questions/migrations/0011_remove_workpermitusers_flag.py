# Generated by Django 3.0.3 on 2020-02-12 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20200212_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workpermitusers',
            name='flag',
        ),
    ]