# Generated by Django 4.2 on 2023-05-31 10:52

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('userview', '0007_image_front_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmbeddedVideoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('video', embed_video.fields.EmbedVideoField()),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]