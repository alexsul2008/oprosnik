# Generated by Django 3.0.3 on 2020-02-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_usersanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersanswer',
            name='otv',
            field=models.IntegerField(default=0, null=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='usersanswer',
            name='vop',
            field=models.IntegerField(default=0, null=True, verbose_name='Вопрос в ответе'),
        ),
    ]