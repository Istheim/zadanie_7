# Generated by Django 4.2.5 on 2023-10-16 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lesson', '0004_subscrib'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='static/lesson', verbose_name='Превью'),
        ),
        migrations.DeleteModel(
            name='Subscrib',
        ),
    ]
