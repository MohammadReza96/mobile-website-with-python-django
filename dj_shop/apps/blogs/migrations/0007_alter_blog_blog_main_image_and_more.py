# Generated by Django 4.1.4 on 2023-04-22 21:34

from django.db import migrations, models
import modules.file_upload_module


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0006_alter_blog_blog_main_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="blog_main_image",
            field=models.ImageField(
                upload_to=modules.file_upload_module.FileUploader.upload_to,
                verbose_name="عکس کاور مقاله",
            ),
        ),
        migrations.AlterField(
            model_name="bloggallary",
            name="blog_image",
            field=models.ImageField(
                upload_to=modules.file_upload_module.FileUploader.upload_to,
                verbose_name="عکس مقاله",
            ),
        ),
    ]