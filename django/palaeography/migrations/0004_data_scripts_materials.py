from django.db import migrations
from palaeography import models


def insert_data_document_material(apps, schema_editor):
    """
    Inserts data into the SlDocumentMaterial select list tables/models
    """

    for name in [
        ["Parchment", "Parchment"],
        ["Papyrus", "Papyrus"],
        ["Leather", "Leather"],
        ["Paper", "Paper"],
        ["Wood", "Wood"],
        ["Metal", "Metal"],
        ["Tree-bark", "Tree-bark"],
        ["Stone", "Stone"]
    ]:
        models.SlDocumentMaterial.objects.create(name_en=name[0], name_fr=name[1])


def insert_data_document_script(apps, schema_editor):
    """
    Inserts data into the SlDocumentScript select list tables/models
    """

    for name in [
        ["Arabic", "Arabic"],
        ["Hebrew", "Hebrew"],
        ["Latin", "Latin"],
    ]:
        models.SlDocumentScript.objects.create(name_en=name[0], name_fr=name[1])


class Migration(migrations.Migration):

    dependencies = [
        ('palaeography', '0003_auto_20230305_0954')
    ]

    operations = [
        migrations.RunPython(insert_data_document_material),
        migrations.RunPython(insert_data_document_script),
    ]
