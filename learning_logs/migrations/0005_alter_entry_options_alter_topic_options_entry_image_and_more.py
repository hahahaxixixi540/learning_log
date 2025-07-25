# Generated by Django 5.2.3 on 2025-07-10 15:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning_logs", "0004_topic_owner"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="entry",
            options={
                "ordering": ["-date_added"],
                "verbose_name": "条目",
                "verbose_name_plural": "条目",
            },
        ),
        migrations.AlterModelOptions(
            name="topic",
            options={
                "ordering": ["-date_added"],
                "verbose_name": "主题",
                "verbose_name_plural": "主题",
            },
        ),
        migrations.AddField(
            model_name="entry",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="可选：上传与条目相关的图片",
                null=True,
                upload_to="entry_images/%Y/%m/%d/",
                verbose_name="条目图片",
            ),
        ),
        migrations.AlterField(
            model_name="entry",
            name="date_added",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="创建时间"
            ),
        ),
        migrations.AlterField(
            model_name="entry",
            name="text",
            field=models.TextField(
                help_text="存储条目详细内容的文本字段", verbose_name="条目内容"
            ),
        ),
        migrations.AlterField(
            model_name="entry",
            name="topic",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="entries",
                to="learning_logs.topic",
                verbose_name="关联主题",
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="date_added",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="创建时间"
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="topics",
                to=settings.AUTH_USER_MODEL,
                verbose_name="所属用户",
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="text",
            field=models.CharField(
                help_text="主题名称最大长度为200个字符",
                max_length=200,
                verbose_name="主题名称",
            ),
        ),
    ]
