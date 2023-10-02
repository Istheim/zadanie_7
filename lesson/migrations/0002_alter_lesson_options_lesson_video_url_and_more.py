# Generated by Django 4.2.5 on 2023-10-02 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
        migrations.AddField(
            model_name='lesson',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на видео'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='preview',
            field=models.ImageField(upload_to='static/lesson', verbose_name='Превью'),
        ),
    ]