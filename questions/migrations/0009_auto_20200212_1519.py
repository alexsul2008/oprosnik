# Generated by Django 3.0.3 on 2020-02-12 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_workpermitusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workpermitusers',
            name='date_passage',
            field=models.DateField(auto_now_add=True, verbose_name='Дата прохождения опроса'),
        ),
    ]