# Generated by Django 4.1.4 on 2023-04-01 20:53

from django.db import migrations, models
import modules.file_upload_module


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sliderimage',
            name='slider_image',
            field=models.FileField(upload_to=modules.file_upload_module.FileUploader.upload_to, verbose_name='عکس اسلایدر'),
        ),
    ]
