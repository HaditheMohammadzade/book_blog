# Generated by Django 4.0.5 on 2023-06-08 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0007_alter_comment_options_rename_body_comment_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
