# Generated by Django 3.0.3 on 2020-02-15 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_auto_20200215_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='vop_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='questions.Questions'),
        ),
    ]
