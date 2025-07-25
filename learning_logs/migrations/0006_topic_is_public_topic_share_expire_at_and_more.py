# Generated by Django 5.2.3 on 2025-07-13 15:22

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "learning_logs",
            "0005_alter_entry_options_alter_topic_options_entry_image_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="is_public",
            field=models.BooleanField(
                default=False,
                help_text="勾选后该主题可通过链接分享给他人",
                verbose_name="是否公开",
            ),
        ),
        migrations.AddField(
            model_name="topic",
            name="share_expire_at",
            field=models.DateTimeField(
                blank=True,
                help_text="可选：设置分享过期时间，为空则永久有效",
                null=True,
                verbose_name="过期时间",
            ),
        ),
        migrations.AddField(
            model_name="topic",
            name="share_password",
            field=models.CharField(
                blank=True,
                help_text="可选：设置访问密码，为空则无需密码",
                max_length=50,
                null=True,
                verbose_name="访问密码",
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="learning_logs.entry",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entry_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="learning_logs.entry",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entry_likes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("entry", "user")},
            },
        ),
    ]
