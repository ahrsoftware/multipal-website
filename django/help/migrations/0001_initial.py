# Generated by Django 3.2.16 on 2022-10-22 15:30

from django.db import migrations, models
import django.db.models.functions.text
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HelpItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, help_text='Must be a valid URL, e.g. https://www.ox.ac.uk', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='help-image')),
                ('video', embed_video.fields.EmbedVideoField(blank=True, help_text='Provide a URL of a video hosted on YouTube or Vimeo, e.g. https://www.youtube.com/watch?v=BHACKCNDMW8', null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='help-pdf')),
                ('visible_only_to_admins', models.BooleanField(default=False)),
                ('admin_published', models.BooleanField(default=True, verbose_name='published')),
                ('admin_notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
    ]
