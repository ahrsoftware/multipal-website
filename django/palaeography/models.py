from django.db import models
from django.urls import reverse
from PIL import Image, ImageOps
from django.core.files import File
from io import BytesIO
from account.models import User
from django.utils import timezone
from django.db.models.functions import Upper
from django.core.validators import MinValueValidator, MaxValueValidator
import os
import textwrap


# Three main sections:
# 1. Reusable code
# 2. Select List Models
# 3. Main models


#
# 1. Reusable code
#


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
    Called by certain models below that have images, e.g. DocumentImage
    """

    if image_field:
        try:
            width, height = Image.open(image_field.path).size
            return True if width > height else False
        except Exception:
            return None
    else:
        return None


def m2m_as_text(m2m_field, delimeter="; "):
    if m2m_field.all():
        return delimeter.join([str(i) for i in m2m_field.all()])
    else:
        return None


class SlAbstract(models.Model):
    """
    An abstract model for Select List models
    See: https://docs.djangoproject.com/en/4.0/topics/db/models/#abstract-base-classes
    """

    name = models.CharField(max_length=1000, db_index=True)

    @property
    def html_details_list_document_text(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = [Upper('name'), 'id']


#
# 2. Select List models
#

class SlDocumentLanguage(SlAbstract):
    "The language/script of a document"


class SlDocumentType(SlAbstract):
    "The type of document. E.g. book"


class SlDocumentInk(SlAbstract):
    "The ink used within a document"


class SlDocumentRepository(SlAbstract):
    "The repository/location of the document. E.g. Cambridge University Library"


#
# 3. Main models
#


class Document(models.Model):
    """
    A historical document (e.g. a book, a coin, etc.)
    """

    m2m_related_name = 'documents'

    name = models.CharField(max_length=1000)
    repositories = models.ManyToManyField(SlDocumentRepository, blank=True, related_name=m2m_related_name, db_index=True)
    shelfmark = models.CharField(max_length=1000, blank=True, null=True)
    type = models.ForeignKey(SlDocumentType, on_delete=models.SET_NULL, blank=True, null=True)
    difficulty = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)])
    languages = models.ManyToManyField(SlDocumentLanguage, blank=True, related_name=m2m_related_name, db_index=True)
    ink = models.ForeignKey(SlDocumentInk, on_delete=models.SET_NULL, blank=True, null=True)
    information = models.TextField(blank=True, null=True)
    custom_instructions = models.TextField(blank=True, null=True, help_text="If the default instructions are insufficient, please provide custom instructions to the user")

    # Partial Date Range
    partial_date_range_from = models.IntegerField(blank=True, null=True)
    partial_date_range_to = models.IntegerField(blank=True, null=True)

    # Date
    date_year = models.IntegerField(blank=True, null=True)
    date_month = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    date_day = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(31)])

    # Time
    time_hour = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(24)])
    time_minute = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(60)])
    time_second = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(60)])

    # Admin
    admin_published = models.BooleanField(default=False, verbose_name='published')
    admin_notes = models.TextField(blank=True, null=True)

    # Metadata
    meta_created_by = models.ForeignKey(User, related_name="document_created_by",
                                        on_delete=models.PROTECT, blank=True, null=True, verbose_name="created by")
    meta_created_datetime = models.DateTimeField(default=timezone.now, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(User, related_name="document_lastupdated_by",
                                            on_delete=models.PROTECT, blank=True, null=True, verbose_name="last updated by")
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    @property
    def instructions(self):
        default_instructions = """XXX TODO
        xxx
        """
        return self.custom_instructions if self.custom_instructions else default_instructions

    @property
    def count_documentimages(self):
        return self.documentimage_set.count()

    @property
    def default_image(self):
        return self.documentimage_set.first()

    @property
    def partial_date_range(self):
        partial_date_range = ""
        # From
        if self.partial_date_range_from:
            partial_date_range += f"From {self.partial_date_range_from} "
        # To
        if self.partial_date_range_to:
            partial_date_range += f"To {self.partial_date_range_to})"
        return partial_date_range if len(partial_date_range) else None

    @property
    def date(self):
        date = ""
        # Year
        if self.date_year:
            date += f"Year {self.date_year}; "
        # Month
        if self.date_month:
            date += f"Month {self.date_month}; "
        # Day
        if self.date_day:
            date += f"Day {self.date_day}; "
        return date if len(date) else None

    @property
    def m2m_as_text_languages(self):
        return m2m_as_text(self.languages)

    @property
    def m2m_as_text_repositories(self):
        return m2m_as_text(self.repositories)

    @property
    def list_title(self):
        return textwrap.shorten(str(self), width=90, placeholder="...")

    @property
    def list_details(self):
        details = f"{singular_plural(self.count_documentimages, 'image')}"
        details += f" | Type: {self.type}" if self.type else ""
        details += f" | Shelfmark: {self.shelfmark}" if self.shelfmark else ""
        details += f" | Difficulty: {self.difficulty}" if self.difficulty else ""
        return textwrap.shorten(details, width=200, placeholder="...")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('palaeography:document-detail', args=[str(self.id)])

    class Meta:
        ordering = [Upper('name'), 'id']


class DocumentImage(models.Model):
    """
    An image belonging to a document, e.g. an image of a page in a book
    """

    m2m_related_name = 'documentimages'

    media_root = 'palaeography/'
    media_dir = media_root + 'documentimages/'
    media_dir_thumbnails = media_dir[:-1] + '-thumbnails/'

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    order_in_document = models.IntegerField(blank=True, null=True)

    image = models.ImageField(upload_to=media_dir)
    image_thumbnail = models.ImageField(upload_to=media_dir_thumbnails, blank=True, null=True)  # Created via save() method below
    right_to_left = models.BooleanField(default=False)

    # Metadata fields
    meta_created_by = models.ForeignKey(User, related_name="documentimage_created_by",
                                        on_delete=models.PROTECT, blank=True, null=True, verbose_name="created by")
    meta_created_datetime = models.DateTimeField(default=timezone.now, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(User, related_name="documentimage_lastupdated_by",
                                            on_delete=models.PROTECT, blank=True, null=True, verbose_name="last updated by")
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    @property
    def other_images_in_document(self):
        return DocumentImage.objects.filter(document=self.document).exclude(id=self.id)

    @property
    def name(self):
        return f"{self.document.name} - Image #{self.order_in_document}"

    @property
    def image_is_wider_than_tall(self):
        return image_is_wider_than_tall(self.image)

    @property
    def alternative_text(self):
        return f"Image of {self.document.name}"

    @property
    def correct_transcription(self):
        transcription_parts = []
        for document_image_part in self.documentimagepart_set.all():
            # Add line break, if needed
            linebreak = '<br>' if document_image_part.is_first_in_line and not document_image_part.is_first_in_image else ''
            # Before
            text_before_part = document_image_part.text_before_part if document_image_part.text_before_part else ''
            text_after_part = document_image_part.text_after_part if document_image_part.text_after_part else ''
            # Add full string to transcription_parts list
            transcription_parts.append(linebreak + text_before_part + document_image_part.text + text_after_part)
        return ' '.join(transcription_parts)

    @property
    def correct_transcription_words(self):
        """
        Returns a matrix (list of lists) of words from correct transcription string
        Each new line in string = a new list within the matrix.
        """
        
        words = []
        for correct_transcription_line in self.correct_transcription.splitlines():
            if len(correct_transcription_line.strip()):
                line = []
                for word in correct_transcription_line.split(' '):
                    line.append({'word': word, 'length': len(word)})
                words.append(line)
        return words

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        When an DocumentImage is saved (created or updated):
        - Set its order in the parent document
        - Create the DocumentImage thumbnail
        """

        # Set the order_in_document with an expected value if it's not been set
        if not self.order_in_document:
            self.order_in_document = self.other_images_in_document.count()

        # Manage image file (compress, thumbnail, etc.)
        super().save(*args, **kwargs)  # Must save now, so image is saved before working with it

        file_extension = self.image.name.split('.')[-1].lower()
        file_format = 'PNG' if file_extension == 'png' else 'JPEG'

        # Create a thumbnail of image (e.g. for use in list views, where many images loaded at once)
        if self.image_thumbnail:
            self.image_thumbnail.delete(save=False)
        img_thumbnail = Image.open(self.image.path)
        img_thumbnail.thumbnail((640, 640))
        img_thumbnail = ImageOps.exif_transpose(img_thumbnail)  # Rotate to correct orientation
        blob_thumbnail = BytesIO()
        img_thumbnail.save(blob_thumbnail, file_format, optimize=True, quality=80)
        name = os.path.basename(self.image.name).rsplit('.', 1)[0]  # removes extension from main image name
        self.image_thumbnail.save(f'{name}_thumbnail.{file_extension}', File(blob_thumbnail), save=False)

        # Update the object (must use update() not save() to avoid unique ID error)
        DocumentImage.objects.filter(id=self.id).update(
            image_thumbnail=f'{self.media_dir_thumbnails}/{name}_thumbnail.{file_extension}'
        )

    class Meta:
        ordering = [Upper('document__name'), 'order_in_document', 'id']


class DocumentImagePart(models.Model):
    """
    A part of an image belonging to a document, e.g. a cut out of a word to be transcribed
    """

    document_image = models.ForeignKey(DocumentImage, on_delete=models.CASCADE)

    # Cropped image measurements
    # left and top are the x,y coordinates of the top-left starting point of the part
    image_cropped_left = models.FloatField(blank=True, null=True)
    image_cropped_top = models.FloatField(blank=True, null=True)
    image_cropped_width = models.FloatField(blank=True, null=True)
    image_cropped_height = models.FloatField(blank=True, null=True)

    text = models.CharField(max_length=1000, blank=True, null=True)
    text_before_part = models.CharField(max_length=1000, blank=True, null=True)
    text_after_part = models.CharField(max_length=1000, blank=True, null=True)
    help_text = models.CharField(max_length=1000, blank=True, null=True)
    cew = models.CharField(max_length=1000, blank=True, null=True)  # TODO - what is this?
    line_index = models.IntegerField()
    part_index_in_line = models.IntegerField()

    # Metadata fields
    meta_created_by = models.ForeignKey(User, related_name="documentimagepart_created_by",
                                        on_delete=models.PROTECT, blank=True, null=True, verbose_name="created by")
    meta_created_datetime = models.DateTimeField(default=timezone.now, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(User, related_name="documentimagepart_lastupdated_by",
                                            on_delete=models.PROTECT, blank=True, null=True, verbose_name="last updated by")
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    @property
    def word_length(self):
        return len(self.text)

    @property
    def is_first_in_image(self):
        return True if self.line_index == 0 and self.part_index_in_line == 0 else False

    @property
    def is_first_in_line(self):
        return True if self.part_index_in_line == 0 else False

    @property
    def line_count(self):
        return self.line_index + 1

    @property
    def part_count_in_line(self):
        return self.part_index_in_line + 1

    class Meta:
        ordering = [Upper('document_image__document__name'), 'document_image__order_in_document', 'document_image__id', 'line_index', 'part_index_in_line', 'id']
