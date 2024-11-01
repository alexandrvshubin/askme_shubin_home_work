# Generated by Django 4.2.16 on 2024-10-29 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_question_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('text_comment', models.TextField(max_length=2000, verbose_name='Text Comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='Publication')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
