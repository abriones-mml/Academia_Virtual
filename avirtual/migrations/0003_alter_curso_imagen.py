# Generated by Django 4.0.4 on 2022-05-24 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avirtual', '0002_alter_curso_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='imagen',
            field=models.ImageField(null=True, upload_to='cursos'),
        ),
    ]
