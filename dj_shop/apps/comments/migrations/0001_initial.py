# Generated by Django 4.1.4 on 2023-03-22 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_alter_brand_brand_image_alter_product_product_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_comment', models.TextField(verbose_name='نظر کاربر')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج نظر')),
                ('is_active', models.BooleanField(default=False, verbose_name='وضعیت نظر')),
                ('comment_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_comments', to='comments.comment', verbose_name='نظر فرعی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_comments', to='products.product', verbose_name='کالا')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_user_comment', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('user_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extra_user_comment', to=settings.AUTH_USER_MODEL, verbose_name='ادمین تایید کننده')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
            },
        ),
    ]
