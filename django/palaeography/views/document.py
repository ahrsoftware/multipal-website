from django.views.generic import (DetailView, ListView, RedirectView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Prefetch
from django.db.models.functions import Coalesce, Upper
from django.urls import reverse
from .. import models
from . import common


class DocumentDetailView(DetailView):
    """
    Class-based view for document detail template
    """
    template_name = 'palaeography/detail.html'
    model = models.Document

    def get_queryset(self):
        queryset = self.model.objects.all()
        # Only show unpublished documents to admins
        if not self.request.user.is_staff:
            queryset = queryset.filter(admin_published=True)
        # Only show documents that have images
        queryset = queryset.annotate(image_count=Count('documentimages')).filter(image_count__gt=0)
        # Prefetch related (M2M) fields
        queryset = queryset.prefetch_related('languages', 'repositories', 'documentimages', 'documentimages__documentimagepart_set')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Admin URL
        context['admin_url'] = reverse('admin:palaeography_document_change', args=[self.object.id])

        # Navigate documents
        # All
        context['navigate_all_url'] = reverse('palaeography:document-list')
        # Previous
        prev = self.get_queryset().filter(id__lt=self.object.id).order_by('id').last()
        if prev:
            context['navigate_previous_url'] = reverse('palaeography:document-detail', args=[prev.id])
        # Next
        next = self.get_queryset().filter(id__gt=self.object.id).order_by('id').first()
        if next:
            context['navigate_next_url'] = reverse('palaeography:document-detail', args=[next.id])

        return context


class DocumentListView(ListView):
    """
    Class-based view for document list template
    """
    template_name = 'palaeography/list.html'
    model = models.Document
    paginate_by = 60

    def get_queryset(self):
        queryset = self.model.objects.all()
        # Only show unpublished documents to admins
        if not self.request.user.is_staff:
            queryset = queryset.filter(admin_published=True)
        # Only show documents that have images
        queryset = queryset.annotate(image_count=Count('documentimages')).filter(image_count__gt=0)
        # Select related (FK) fields
        queryset = queryset.select_related('type')
        # Prefetch related (M2M) fields
        queryset = queryset.prefetch_related(
            Prefetch(
                'documentimages',
                queryset=models.DocumentImage.objects.select_related('difficulty')
            ), 'languages', 'inks', 'repositories', 'documentimages', 'documentimages__documentimagepart_set')
        # Annotations
        queryset = queryset.annotate(
            # year_ annotations used for filtering on multiple fields storing year data
            year_min=Coalesce('date_year', 'partial_date_range_year_from'),
            year_max=Coalesce('date_year', 'partial_date_range_year_to')
        )
        # Search
        search = self.request.GET.get('search', '')
        if search != '':
            queryset = queryset.filter(
                # Char
                Q(name__icontains=search) |
                Q(shelfmark__icontains=search) |
                Q(information__icontains=search) |
                # Integer
                Q(partial_date_range_year_from__icontains=search) |
                Q(partial_date_range_year_to__icontains=search) |
                Q(date_year__icontains=search) |
                Q(date_month__icontains=search) |
                Q(date_day__icontains=search) |
                # FK
                Q(type__name_en__icontains=search) |
                Q(type__name_fr__icontains=search) |
                # M2M
                Q(inks__name_en__icontains=search) |
                Q(inks__name_fr__icontains=search) |
                Q(languages__name_en__icontains=search) |
                Q(languages__name_fr__icontains=search) |
                Q(repositories__name_en__icontains=search) |
                Q(repositories__name_fr__icontains=search) |
                # Via related models
                Q(documentimages__difficulty__name_en__icontains=search) |
                Q(documentimages__difficulty__name_fr__icontains=search)
            )
        # Filter
        queryset = common.filter(self.request, queryset)
        # Sort
        queryset = common.sort(self.request, queryset)
        # Remove any possible duplicates
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Documents'
        context['filter_pre'] = common.filter_pre
        context['filter_pre_gt'] = common.filter_pre_gt
        context['filter_pre_lt'] = common.filter_pre_lt
        context['list_type'] = 'text'

        # Options: Sort By
        context['options_sortby'] = [
            # Alphabetical
            {
                'value': 'name',
                'label': 'Name'
            },
            {
                'value': 'shelfmark',
                'label': 'Shelfmark'
            },
            {
                'value': 'year_min',
                'label': 'Year'
            },
            {
                'value': 'meta_created_datetime',
                'label': 'Date Added to MultiPal'
            },
            {
                'value': 'meta_lastupdated_datetime',
                'label': 'Date Updated in MultiPal'
            },
            # Numerical
            {
                'value': f'{common.sort_pre_count_value}documentimages',
                'label': f'{common.sort_pre_count_label}Images'
            },
        ]

        # Options: Filters
        order_by_lang_field = Upper('name_' + self.request.LANGUAGE_CODE)
        context['options_filters'] = [
            {
                'filter_id': f'{common.filter_pre_mm}languages',
                'filter_name': 'Language',
                'filter_options': models.SlDocumentLanguage.objects.all().order_by(order_by_lang_field)
            },
            {
                'filter_id': f'{common.filter_pre_fk}documentimages__difficulty',
                'filter_name': 'Difficulty',
                'filter_options': models.SlDocumentImageDifficulty.objects.all().order_by('id')
            },
            {
                'filter_id': f'{common.filter_pre_fk}type',
                'filter_name': 'Type',
                'filter_options': models.SlDocumentType.objects.all().order_by(order_by_lang_field)
            },
            {
                'filter_id': f'{common.filter_pre_mm}inks',
                'filter_name': 'Ink',
                'filter_options': models.SlDocumentInk.objects.all().order_by(order_by_lang_field)
            },
            {
                'filter_id': f'{common.filter_pre_mm}repositories',
                'filter_name': 'Repository',
                'filter_options': models.SlDocumentRepository.objects.all().order_by(order_by_lang_field)
            },
            {
                'filter_id': f'{common.filter_pre_gt}year_min',
                'filter_name': 'Year (from)',
                'filter_number_min': -2000,
                'filter_number_max': 2000
            },
            {
                'filter_id': f'{common.filter_pre_lt}year_max',
                'filter_name': 'Year (to)',
                'filter_number_min': -2000,
                'filter_number_max': 2000
            },
        ]

        return context


class DocumentImagePartAddRedirectView(LoginRequiredMixin, RedirectView):
    """
    Class-based view for adding a new document image part and redirecting to parent document
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # Calculate line_index and part_index_in_line values
        new_line = self.request.POST.get('newline')
        add_after_image_part_id = self.request.POST.get('add_after_image_part_id')
        # If adding after an existing part
        if add_after_image_part_id:
            add_after_part = models.DocumentImagePart.objects.get(id=add_after_image_part_id)
            # Move to a new line after the specified part
            if new_line:
                part_index_in_line = 0
                line_index = add_after_part.line_index + 1
            # Add within current line after specified part
            else:
                part_index_in_line = add_after_part.part_index_in_line + 1
                line_index = add_after_part.line_index
        # If adding to start
        else:
            line_index = 0
            part_index_in_line = 0

        # Save DocumentImagePart object
        document_image_part_obj = models.DocumentImagePart.objects.create(
            document_image_id=self.request.POST.get('document_image_id'),
            # Cropped image measurements
            image_cropped_left=self.request.POST.get('image_cropped_left'),
            image_cropped_top=self.request.POST.get('image_cropped_top'),
            image_cropped_width=self.request.POST.get('image_cropped_width'),
            image_cropped_height=self.request.POST.get('image_cropped_height'),
            # Index/order in solution (by line, part)
            line_index=line_index,
            part_index_in_line=part_index_in_line,
            # Content
            text=self.request.POST.get('text')
        )
        # Optional fields
        document_image_part_obj.text_before_part = self.request.POST.get('text_before_part')
        document_image_part_obj.text_after_part = self.request.POST.get('text_after_part')
        document_image_part_obj.help_text = self.request.POST.get('help_text')
        document_image_part_obj.cew = self.request.POST.get('cew')
        document_image_part_obj.save()

        # Update other parts in response to this new part
        document_image_part_obj.move_other_parts_positions(add_after_image_part_id, delete=False, new_line=new_line == 'on')

        # Return to document page
        document_id = document_image_part_obj.document_image.document_id
        return f"{reverse('palaeography:document-detail', args=[document_id])}?image={document_image_part_obj.document_image_id}"


class DocumentImagePartDeleteRedirectView(LoginRequiredMixin, RedirectView):
    """
    Class-based view for deleting a document image part and redirecting to parent document
    """

    def get_redirect_url(self, *args, **kwargs):
        document_image_part_obj = models.DocumentImagePart.objects.get(id=self.request.POST.get('delete_document_image_part_id'))
        # Move the position of affect parts assuming this part has been deleted
        document_image_part_obj.move_other_parts_positions(delete=True)
        # Delete this part
        document_image_part_obj.delete()
        # Return to document page
        return f"{reverse('palaeography:document-detail', args=[self.request.POST.get('document_id')])}?image={document_image_part_obj.document_image_id}"
