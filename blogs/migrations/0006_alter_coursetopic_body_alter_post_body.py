# Generated by Django 5.0.6 on 2024-06-08 07:44

import django_editorjs.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetopic',
            name='body',
            field=django_editorjs.fields.EditorJsField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_editorjs.fields.EditorJsField(default=True),
            preserve_default=False,
        ),
    ]
