# Generated by Django 4.1.4 on 2023-03-29 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'نظر در مورد کالا ها', 'verbose_name_plural': 'نظرات در مورد کالا ها'},
        ),
    ]