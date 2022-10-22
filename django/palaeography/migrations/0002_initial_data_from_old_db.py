from django.conf import settings
from django.db import migrations
from palaeography import models
import os
from ast import literal_eval


# Reusable functions/variables

old_data = os.path.join(settings.BASE_DIR, 'palaeography', 'migrations', 'old_data')


def set_related_values(data_file, main_model, relationship_type):
    """
    data_file = a .txt file containing a list of objects
    main_model = the model of the object for which the data is being set, e.g. models.Document
    relationship_type = 'fk' or 'm2m'
    """
    for object_dict in literal_eval(data_file.read()):
        # Get the main model object
        object = main_model.objects.get(id=object_dict['id'])
        # Loop through key/value pairs in object dictionary (other than the id field)
        for field, value in object_dict.items():
            if field != 'id':
                # Get the related object
                related_object = models.Document._meta.get_field(field).related_model.objects.get_or_create(name=value)[0]
                # Set related field value based on relationship type (either FK or M2m)
                if relationship_type == 'fk':
                    setattr(object, field, related_object)
                elif relationship_type == 'm2m':
                    getattr(object, field).add(related_object)
        # Save changes to the object
        object.save()


# Migration functions


def insert_data_select_list_models(apps, schema_editor):
    """
    Inserts data into the new select list tables/models in this new database

    FK data is also inserted below using get_or_create, but sometimes it's
    required to manually set additional values, e.g. those that appear in
    the old website's user interface but aren't in the old database
    """

    # SlDocumentType
    for name in [
        "livre",
        "document",
        "épigraphie",
        "numismatique"
    ]:
        models.SlDocumentType.objects.create(name=name)


def insert_data_documents(apps, schema_editor):
    """
    Inserts data into the Document model
    """

    with open(os.path.join(old_data, "data_documents.txt"), 'r') as file:
        for object in literal_eval(file.read()):
            models.Document.objects.create(**object)


def insert_data_documents_fk(apps, schema_editor):
    """
    Inserts data for foreign key fields in the Document model
    """

    with open(os.path.join(old_data, "data_documents_fk.txt"), 'r') as file:
        set_related_values(file, models.Document, 'fk')


def insert_data_documents_m2m(apps, schema_editor):
    """
    Inserts data for many to many fields in the Document model
    """

    with open(os.path.join(old_data, "data_documents_m2m.txt"), 'r') as file:
        set_related_values(file, models.Document, 'm2m')


def insert_data_documentimages(apps, schema_editor):
    """
    Inserts data into the Document Image model
    """

    with open(os.path.join(old_data, "data_documentimages.txt"), 'r') as file:
        for object in literal_eval(file.read()):
            models.DocumentImage.objects.create(**object)


def insert_data_documentimageparts(apps, schema_editor):
    """
    Inserts data into the Document Image Part model
    """

    with open(os.path.join(old_data, "data_documentimageparts.txt"), 'r') as file:
        for object in literal_eval(file.read()):
            models.DocumentImagePart.objects.create(**object)


class Migration(migrations.Migration):

    dependencies = [
        ('palaeography', '0001_initial')
    ]

    operations = [
        migrations.RunPython(insert_data_select_list_models),
        migrations.RunPython(insert_data_documents),
        migrations.RunPython(insert_data_documents_fk),
        migrations.RunPython(insert_data_documents_m2m),
        migrations.RunPython(insert_data_documentimages),
        migrations.RunPython(insert_data_documentimageparts),
    ]
