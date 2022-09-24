from django.db import models
from django.urls import reverse
from PIL import Image
from django.core.files import File
from io import BytesIO
from .apps import app_name
from account.models import User
from django.utils import timezone
from django.db.models.functions import Upper
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import json
import textwrap


# Three main sections:
# 1. Reusable code
# 2. Select List Models
# 3. Main models
# 4. Search Fields


#
# 1. Reusable code
#


def url_detail(object):
    """
    Return a URL for the detail page of the passed object
    """
    return reverse(f'{app_name}:{object.__class__.__name__.lower()}-detail', kwargs={'pk': object.id})


def singular_plural(count, word_singular, word_plural=None):
    """
    Returns a string of the count and either the singular or plural version of the word
    Used a lot in the model in list_details() methods, for correctly displaying counts
    E.g. 1 script instead of 1 scripts
    """

    if word_plural is None:
        # Add 's' to singular, unless singular ends in 'y' (then replace 'y' with 'ies') e.g. entity -> entities
        word_plural = f'{word_singular}s' if word_singular[-1] != 'y' else f'{word_singular[0:-1]}ies'
    return f'{count} {word_singular}' if count == 1 else f'{count} {word_plural}'


def image_is_wider_than_tall(image_field):
    """
    Takes in a Django image_field
    Returns:
        - True, if the image is wider than it is tall (height > width)
        - False, if the image is taller than it is wide (width > height)
        - None, if imagefield has no image
    Called by certain models below that have images, e.g. ItemImage
    """

    if image_field:
        try:
            width, height = Image.open(image_field.path).size
            return True if width > height else False
        except Exception:
            return None
    else:
        return None


def queryset_as_string(queryset, separator=", "):
    """
    Return a queryset as a string with the specified separator. E.g. "Item 1, Item 2, Item 3"
    """
    return separator.join([str(obj) for obj in queryset]) if len(queryset) else None


class SlAbstract(models.Model):
    """
    An abstract model for Select List models
    See: https://docs.djangoproject.com/en/4.0/topics/db/models/#abstract-base-classes
    """

    name = models.CharField(max_length=1000, db_index=True)

    @property
    def html_details_list_item_text(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = [Upper('name'), 'id']


#
# 2. Select List models
#


# class SlDateCentury(SlAbstract):
#     "Select List model used by Item and Work models - A century in CE e.g. 1st Century CE"

#     century_number = models.IntegerField(validators=[MaxValueValidator(21), MinValueValidator(1)])

#     @property
#     def html_select_value_field(self):
#         "Field to use as value in <option value=''> for select html elements (default = 'id')"
#         return self.century_number

#     class Meta:
#         ordering = ['century_number']


# class SlCountry(SlAbstract):
#     "Select List model used by SlTown model - A country in which a town (from SlTown) exists"

#     class Meta:
#         verbose_name = 'Country'
#         verbose_name_plural = 'Countries'


# class SlTown(SlAbstract):
#     "Select List model used by SlLibrary model - A town/city in which a library (from SlLibrary) exists"

#     country = models.ForeignKey(SlCountry, on_delete=models.SET_NULL, blank=True, null=True)

#     @property
#     def data_hierarchy_parents_ids(self):
#         """
#         Used to determine parent options in filter select lists in list.html
#         E.g. when a parent option is selected, this object will be shown in the child list
#         Also see 'Data hierarchy properties' in views for related code
#         """
#         return str(json.dumps({'country': self.country.id}))

#     def __str__(self):
#         return f"{self.name}, {self.country}" if self.country else self.name

#     class Meta:
#         verbose_name = 'Town/City'
#         verbose_name_plural = 'Towns/Cities'


# class SlLibrary(SlAbstract):
#     "Select List model used by Item model - A library in which the item exists"

#     town = models.ForeignKey(SlTown, on_delete=models.SET_NULL, blank=True, null=True)

#     @property
#     def data_hierarchy_parents_ids(self):
#         """
#         Used to determine parent options in filter select lists in list.html
#         E.g. when a parent option is selected, this object will be shown in the child list
#         Also see 'Data hierarchy properties' in views for related code
#         """
#         return str(json.dumps({
#             'country': self.town.country.id,
#             'town': self.town.id
#         }))

#     def __str__(self):
#         return f"{self.name} ({self.town})" if self.town else self.name

#     class Meta:
#         verbose_name = 'Library'
#         verbose_name_plural = 'Libraries'


# class SlItemShelfmark(SlAbstract):
#     "Select List model used by Item model - A shelfmark (aka name, identifier) of the item, which can be used to group similar items"


# class SlItemCategory(SlAbstract):
#     "Select List model used by Item model - A category of item (e.g. a manuscript book, document, etc.)"


# class SlItemCodicologicalDefinition(SlAbstract):
#     "Select List model used by Item model - Codicological definition"


# class SlItemFormat(SlAbstract):
#     "Select List model used by Item model - Format"



#
# 3. Main models
#


# class Item(models.Model):
#     """
#     An item (e.g. a manuscript, document, etc.)
#     """

#     m2m_related_name = 'items'

#     shelfmark = models.ForeignKey(SlItemShelfmark, on_delete=models.RESTRICT)
#     name = models.CharField(max_length=1000, blank=True, help_text='(Optional) will be appended to the shelfmark to form the title of this Item')
#     library = models.ForeignKey(SlLibrary, on_delete=models.SET_NULL, blank=True, null=True)
#     category = models.ForeignKey(SlItemCategory, on_delete=models.RESTRICT, verbose_name='item category')
#     description = models.TextField(blank=True, null=True)
#     keywords = models.ManyToManyField(SlKeyword, blank=True, related_name=m2m_related_name, db_index=True)

#     # Codicological/Document Definition
#     codicological_definition = models.ForeignKey(SlItemCodicologicalDefinition, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Codicological definition")
#     format = models.ForeignKey(SlItemFormat, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Format")
#     format_other = models.CharField(max_length=1000, blank=True, verbose_name="Format (other)")
#     type_of_manuscript = models.ForeignKey(SlItemTypeOfManuscript, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Type of manuscript")
#     codicological_definition_observations = models.TextField(blank=True, null=True, verbose_name="Codicological definition observations")
#     document_definition = models.ForeignKey(SlItemDocumentDefinition, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Document definition")
#     document_definition_observations = models.TextField(blank=True, null=True, verbose_name="Document definition observations")

#     # Miscellaneous
#     manuscript_history = models.TextField(blank=True, null=True, verbose_name="Manuscript history")
#     bibliography = models.TextField(blank=True, null=True, verbose_name="Bibliography")

#     # Admin
#     admin_published = models.BooleanField(default=False, verbose_name='published')
#     admin_notes = models.TextField(blank=True, null=True)

#     # Metadata
#     meta_editors = models.ManyToManyField(User,
#                                           related_name=m2m_related_name + '_editors',
#                                           blank=True,
#                                           verbose_name='editors')
#     meta_contributors = models.ManyToManyField(User,
#                                                related_name=m2m_related_name + '_contributors',
#                                                blank=True,
#                                                verbose_name='contributors')
#     meta_created_by = models.ForeignKey(User, related_name="item_created_by",
#                                         on_delete=models.PROTECT, blank=True, null=True, verbose_name="created by")
#     meta_created_datetime = models.DateTimeField(default=timezone.now, verbose_name="created")
#     meta_lastupdated_by = models.ForeignKey(User, related_name="item_lastupdated_by",
#                                             on_delete=models.PROTECT, blank=True, null=True, verbose_name="last updated by")
#     meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")
#     meta_firstpublished_datetime = models.DateTimeField(blank=True, null=True, verbose_name="first published")

#     @property
#     def itemimages(self):
#         return self.itemimage_set.filter(admin_published=True)

#     @property
#     def count_itemimages(self):
#         return self.itemimages.count()

#     @property
#     def url_detail(self):
#         return url_detail(self)

#     @property
#     def list_title(self):
#         return textwrap.shorten(str(self), width=90, placeholder="...")

#     @property
#     def list_details(self):
#         details = f"{singular_plural(self.count_itemimages, 'image')}"
#         details += f" | Category: {self.category}" if self.category else ""
#         details += f" | Date: {self.date_century}" if self.date_century else ""
#         details += f" | Located in: {self.library}" if self.library else ""
#         return textwrap.shorten(details, width=200, placeholder="...")

#     def __str__(self):
#         return f'{self.shelfmark.name} ({self.name})' if self.name else self.shelfmark.name

#     def get_absolute_url(self):
#         return reverse('palaeography:item-detail', args=[str(self.id)])

#     class Meta:
#         ordering = [Upper('shelfmark__name'), Upper('name'), 'id']


#
# 4. Search fields: Fields used in search (used in admin.py, views, etc)
#


# Item
search_fields_item = ['shelfmark__name',
                      'name',
                      'category__name',
                      'library__name',
                      'library__town__name',
                      'library__town__country__name',
                      'keywords__name',
                      'date_century__name',
                      'codicological_definition__name',
                      'format__name',
                      'type_of_manuscript__name',
                      'document_definition__name',
                      'state_of_item__name',
                      'state_of_material__name',
                      'state_of_writing__name',
                      'palimpsest__name',
                      'pricking__name',
                      'pricking_instrument__name',
                      'pricking_pattern__name',
                      'ruling__name',
                      'ruling_method__name',
                      'ruling_pattern__name',
                      'script_type__name',
                      'script_mode__name',
                      'script_quality__name',
                      'script_function__name',
                      'script_style__name',
                      'vocalization__name',
                      'abbreviations__name',
                      'invocation__name',
                      'binding__name',
                      'type_of_sewing__name']
