from django.conf import settings
from django.db import migrations
from palaeography import models
from ast import literal_eval
from html.parser import HTMLParser
from io import StringIO
import os
import shutil


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
                related_object = models.Document._meta.get_field(field).related_model.objects.get_or_create(name_en=value)[0]
                # Set related field value based on relationship type (either FK or M2m)
                if relationship_type == 'fk':
                    setattr(object, field, related_object)
                elif relationship_type == 'm2m':
                    getattr(object, field).add(related_object)
        # Save changes to the object
        object.save()


class MLStripper(HTMLParser):
    """
    Required by below strip_html_tags() function to remove HTML tags from a string
    """
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


def strip_html_tags(html):
    """
    Removes HTML tags from strings, e.g. <p>xxxx</p> --> xxxx
    Used for fields that were a RichTextField in old db but a plain TextField in the new db
    """
    if html:
        # Add new lines to </p> tags before they're removed, to preserve new lines in output
        html = html.replace('<p>', '<p>\n')
        # Strip HTML tags from string and return
        stripper = MLStripper()
        stripper.feed(html)
        return stripper.get_data().strip()


# Migration functions


def insert_data_select_list_models(apps, schema_editor):
    """
    Inserts data into the new select list tables/models in this new database

    FK data is also inserted below using get_or_create, but sometimes it's
    required to manually set additional values, e.g. those that appear in
    the old website's user interface but aren't in the old database
    """

    # SlDocumentInk
    for name in [
        ["Dark brown", "Brune foncé"],
        ["Brown", "Brun"],
        ["Light brown", "Brun clair"],
        ["Red", "Rouge"],
        ["Black", "Noir"]
    ]:
        models.SlDocumentInk.objects.create(name_en=name[0], name_fr=name[1])

    # SlDocumentLanguage
    for name in [
        ["Arabic", "FR1"],
        ["Aramaic", "FR2"],
        ["Chinese", "FR3"],
        ["Cop", "FR4"],
        ["Egyptian", "FR5"],
        ["Geʽez", "FR6"],
        ["Greek", "FR7"],
        ["Hebrew", "FR8"],
        ["Latin", "FR9"],
        ["Russian", "FR10"],
        ["Sanskrit", "FR11"]
    ]:
        models.SlDocumentLanguage.objects.create(name_en=name[0], name_fr=name[1])

    # SlDocumentRepository
    for name in [
        [
            "Angelicanus graecus 65, f. 153v",
            "Angelicanus graecus 65, f. 153v"
        ],
        [
            "Ann Arbor, Michigan University",
            "Ann Arbor, Michigan University"
        ],
        [
            "Archive d’État de Venise",
            "Archive d’État de Venise"
        ],
        [
            "Berlin",
            "Berlin"
        ],
        [
            "Berlin, Ägyptisches Museum P. 13500",
            "Berlin, Ägyptisches Museum P. 13500"
        ],
        [
            "Biblioteca Angelica, Rome",
            "Biblioteca Angelica, Rome"
        ],
        [
            "Bibliothèque de l'Université de Cambridge",
            "Bibliothèque de l'Université de Cambridge"
        ],
        [
            "Bibliothèque nationale et universitaire de Strasbourg",
            "Bibliothèque nationale et universitaire de Strasbourg"
        ],
        [
            "Bodleian Library (Oxford, Angleterre)",
            "Bodleian Library (Oxford, Angleterre)"
        ],
        [
            "Bologna, Archivio di Stato",
            "Bologna, Archivio di Stato"
        ],
        [
            "British Library, UK London",
            "British Library, UK London"
        ],
        [
            "British Museum",
            "British Museum"
        ],
        [
            "Bruxelles, Musées royaux d’Art et d’Histoire",
            "Bruxelles, Musées royaux d’Art et d’Histoire"
        ],
        [
            "Cairo, French Institute for Oriental Archaeology",
            "Cairo, French Institute for Oriental Archaeology"
        ],
        [
            "Cambridge University Library",
            "Cambridge University Library"
        ],
        [
            "Cambridge University Library: Taylor-Schechter Cairo Genizah Collection",
            "Cambridge University Library: Taylor-Schechter Cairo Genizah Collection"
        ],
        [
            "Codex Atheniensis Museum Benaki TA 194",
            "Codex Atheniensis Museum Benaki TA 194"
        ],
        [
            "Codex Parisinus Supplementum graecum 1158, f. 133v",
            "Codex Parisinus Supplementum graecum 1158, f. 133v"
        ],
        [
            "Collège de la Sainte Famille, Le Caire, Egypte",
            "Collège de la Sainte Famille, Le Caire, Egypte"
        ],
        [
            "Colmar, Bibliothèque municipale",
            "Colmar, Bibliothèque municipale"
        ],
        [
            "Cologne, Stadtarchiv",
            "Cologne, Stadtarchiv"
        ],
        [
            "Florence, Biblioteca Medicea Laurenziana",
            "Florence, Biblioteca Medicea Laurenziana"
        ],
        [
            "Fribourg",
            "Fribourg"
        ],
        [
            "Greenwich, National Maritime Museum",
            "Greenwich, National Maritime Museum"
        ],
        [
            "Heidelberg, Institut für Papyrologie",
            "Heidelberg, Institut für Papyrologie"
        ],
        [
            "Institut français d'archéologie orientale (IFAO), Cairo",
            "Institut français d'archéologie orientale (IFAO), Cairo"
        ],
        [
            "Israël",
            "Israël"
        ],
        [
            "La collection Mosseri est déposée à la Cambridge University Library maintenant",
            "La collection Mosseri est déposée à la Cambridge University Library maintenant"
        ],
        [
            "Le Caire, Institut Français d'Archéologie Orientale",
            "Le Caire, Institut Français d'Archéologie Orientale"
        ],
        [
            "Library of the hungarian academy of sciences budapest",
            "Library of the hungarian academy of sciences budapest"
        ],
        [
            "London, British Library",
            "London, British Library"
        ],
        [
            "London, British Museum",
            "London, British Museum"
        ],
        [
            "Milan, Università Statale",
            "Milan, Università Statale"
        ],
        [
            "Monè tês Hagias Êkaterinès, Mont Sinai",
            "Monè tês Hagias Êkaterinès, Mont Sinai"
        ],
        [
            "Musée Carnavalet",
            "Musée Carnavalet"
        ],
        [
            "Muséum d'histoire naturelle de Lyon",
            "Muséum d'histoire naturelle de Lyon"
        ],
        [
            "New Haven, Yale University, Beinecke Rare Book and Manuscript Library",
            "New Haven, Yale University, Beinecke Rare Book and Manuscript Library"
        ],
        [
            "New York, Metropolitan Museum of Art",
            "New York, Metropolitan Museum of Art"
        ],
        [
            "Oxford, Sackler Library",
            "Oxford, Sackler Library"
        ],
        [
            "Paris",
            "Paris"
        ],
        [
            "Paris, Bibliothèque Nationale de France",
            "Paris, Bibliothèque Nationale de France"
        ],
        [
            "Paris, Bibliothèque Nationale de France: Département des Monnaies, Médailles et Antiques",
            "Paris, Bibliothèque Nationale de France: Département des Monnaies, Médailles et Antiques"
        ],
        [
            "Paris, Louvre",
            "Paris, Louvre"
        ],
        [
            "Paris, Sorbonne, Institut de Papyrologie",
            "Paris, Sorbonne, Institut de Papyrologie"
        ],
        [
            "Riga. Archives nationales historiques",
            "Riga. Archives nationales historiques"
        ],
        [
            "Turin",
            "Turin"
        ],
        [
            "Vienna, Austrian National Library",
            "Vienna, Austrian National Library"
        ],
        [
            "Westminster Abbey Library and Archive, Londres, Grande Bretagne",
            "Westminster Abbey Library and Archive, Londres, Grande Bretagne"
        ],
        [
            "cgb.fr",
            "cgb.fr"
        ],
        [
            "in situ",
            "in situ"
        ],
        [
            "Ägyptisches Museum und Papyrussammlung, Berlin",
            "Ägyptisches Museum und Papyrussammlung, Berlin"
        ]
    ]:
        models.SlDocumentRepository.objects.create(name_en=name[0], name_fr=name[1])

    # SlDocumentType
    for name in [
        ["Book", "Livre"],
        ["Document", "Document"],
        ["Epigraphy", "Épigraphie"],
        ["Numismatics", "Numismatique"]
    ]:
        models.SlDocumentType.objects.create(name_en=name[0], name_fr=name[1])

    # SlDocumentImageDifficulty
    for name in [
        ["Easy", "Facile"],
        ["Normal", "Normale"],
        ["Hard", "Difficile"]
    ]:
        models.SlDocumentImageDifficulty.objects.create(name_en=name[0], name_fr=name[1])


def insert_data_documents(apps, schema_editor):
    """
    Inserts data into the Document model
    """

    with open(os.path.join(old_data, "data_documents.txt"), 'r') as file:
        for object in literal_eval(file.read()):

            # Tidy information data
            object['information'] = strip_html_tags(object['information'])

            # Save object
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

    # Delete thumbnail directory and the existing images in them, to start fresh
    try:
        shutil.rmtree(os.path.join(settings.BASE_DIR, f"media/palaeography/documentimages-thumbnails"))
    except FileNotFoundError:
        pass  # it's ok if can't find dir, will just skip it

    with open(os.path.join(old_data, "data_documentimages.txt"), 'r') as file:
        for object in literal_eval(file.read()):

            # Tidy custom_instructions data
            object['custom_instructions'] = strip_html_tags(object['custom_instructions'])

            # Save object
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
