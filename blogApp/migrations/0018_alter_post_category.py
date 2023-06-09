# Generated by Django 4.0.5 on 2023-06-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0017_category_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, choices=[('ravan', 'رشد فردی'), ('iran', 'ادبیات ایران'), ('russ', 'ادبیات روس'), ('eng', 'ادبیات انگلیسی'), ('france', 'ادبیات فرانسه')], max_length=1000, null=True),
        ),
    ]