# Generated by Django 3.0.3 on 2020-02-05 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, verbose_name='Пользователь')),
                ('group_user', models.CharField(max_length=50, verbose_name='Группа пользователя')),
                ('session_key', models.CharField(max_length=150, verbose_name='Сессия пользователя')),
                ('not_ok_vop', models.IntegerField(default=0, null=True, verbose_name='Не правильный вопрос')),
                ('not_ok_otv', models.IntegerField(default=0, null=True, verbose_name='Не правильный ответ')),
                ('ok_vop', models.IntegerField(default=0, null=True, verbose_name='Правильный вопрос')),
                ('ok_otv', models.IntegerField(default=0, null=True, verbose_name='Правильный ответ')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Вопрос')),
                ('in_active', models.BooleanField(default=True, verbose_name='Активность вопроса')),
                ('image', models.ImageField(blank=True, upload_to='guestions/', verbose_name='Изображение')),
                ('doc_url', models.CharField(blank=True, max_length=250, verbose_name='Ссылка на документ')),
                ('groups', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group', verbose_name='группа отдела')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Текст ответа')),
                ('approved', models.BooleanField(default=False, verbose_name='Правильность ответа')),
                ('vop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Questions')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]
