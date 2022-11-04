# Generated by Django 3.2.16 on 2022-11-04 20:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('shelfmark', models.CharField(blank=True, max_length=1000, null=True)),
                ('information', models.TextField(blank=True, null=True)),
                ('custom_instructions', models.TextField(blank=True, help_text='If the default instructions are insufficient, please provide custom instructions to the user', null=True)),
                ('partial_date_range_from', models.IntegerField(blank=True, null=True)),
                ('partial_date_range_to', models.IntegerField(blank=True, null=True)),
                ('date_year', models.IntegerField(blank=True, null=True)),
                ('date_month', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('date_day', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('time_hour', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)])),
                ('time_minute', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(60)])),
                ('time_second', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(60)])),
                ('admin_published', models.BooleanField(default=False, verbose_name='published')),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('meta_created_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(blank=True, null=True, verbose_name='last updated')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='DocumentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_in_document', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='palaeography/documentimages/')),
                ('image_thumbnail', models.ImageField(blank=True, null=True, upload_to='palaeography/documentimages-thumbnails/')),
                ('right_to_left', models.BooleanField(default=False)),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palaeography.document')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('document__name'), 'order_in_document', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlDocumentDifficulty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlDocumentInk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlDocumentLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlDocumentRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlDocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentImagePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_cropped_left', models.FloatField(blank=True, null=True)),
                ('image_cropped_top', models.FloatField(blank=True, null=True)),
                ('image_cropped_width', models.FloatField(blank=True, null=True)),
                ('image_cropped_height', models.FloatField(blank=True, null=True)),
                ('text', models.CharField(blank=True, max_length=1000, null=True)),
                ('text_before_part', models.CharField(blank=True, max_length=1000, null=True)),
                ('text_after_part', models.CharField(blank=True, max_length=1000, null=True)),
                ('help_text', models.CharField(blank=True, max_length=1000, null=True)),
                ('cew', models.CharField(blank=True, max_length=1000, null=True)),
                ('line_index', models.IntegerField()),
                ('part_index_in_line', models.IntegerField()),
                ('meta_created_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(blank=True, null=True, verbose_name='last updated')),
                ('document_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palaeography.documentimage')),
                ('meta_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='documentimagepart_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('meta_lastupdated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='documentimagepart_lastupdated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('document_image__document__name'), 'document_image__order_in_document', 'document_image__id', 'line_index', 'part_index_in_line', 'id'],
            },
        ),
        migrations.AddField(
            model_name='document',
            name='difficulty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='palaeography.sldocumentdifficulty'),
        ),
        migrations.AddField(
            model_name='document',
            name='ink',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='palaeography.sldocumentink'),
        ),
        migrations.AddField(
            model_name='document',
            name='languages',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='palaeography.SlDocumentLanguage'),
        ),
        migrations.AddField(
            model_name='document',
            name='meta_created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='document',
            name='meta_lastupdated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_lastupdated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
        migrations.AddField(
            model_name='document',
            name='repositories',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='palaeography.SlDocumentRepository'),
        ),
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='palaeography.sldocumenttype'),
        ),
    ]
