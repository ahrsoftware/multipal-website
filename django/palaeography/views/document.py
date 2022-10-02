from django.views.generic import (DetailView, ListView)
from django.urls import reverse
from .. import models
from . import common


class DocumentDetailView(DetailView):
    """
    Class-based view for item detail template
    """
    template_name = 'palaeography/detail.html'
    model = models.Document

#     def get_queryset(self):
#         return common.filter_by_user_role_permissions_view(self, self.model.objects.all())

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Admin URL
#         context['admin_url'] = reverse('admin:palaeography_item_change', args=[self.object.id])

#         # Related data
#         context['related_data_list'] = [
#             {
#                 'title': 'Document Images',
#                 'id': 'itemimages',
#                 'list_type': 'image',
#                 'objects': common.filter_by_user_role_permissions_view(self, self.object.itemimages)
#             },
#             {
#                 'title': 'Other Documents in Shelfmark',
#                 'id': 'otheritemsinshelfmark',
#                 'list_type': 'text',
#                 'objects': common.filter_by_user_role_permissions_view(
#                     self,
#                     models.Document.objects.filter(
#                         admin_published=True,
#                         shelfmark=self.object.shelfmark).exclude(id=self.object.id)
#                 )
#             },
#         ]

#         return context


class DocumentListView(ListView):
    """
    Class-based view for item list template
    """
    template_name = 'palaeography/list.html'
    model = models.Document
    paginate_by = common.PAGINATE_COUNT

#     def get_queryset(self):
#         # Initially filter by the current user's role's permissions
#         queryset = common.filter_by_user_role_permissions_view(self, self.model.objects.filter(admin_published=True))
#         # Select related (FK) fields
#         queryset = queryset.select_related('shelfmark', 'category', 'date_century', 'library__town__country',)
#         # Search
#         queryset = common.search(self.request, queryset, models.search_fields_item)
#         # Filter
#         queryset = common.filter(self.request, queryset)
#         # Sort
#         queryset = common.sort(self.request, queryset)
#         # Remove any possible duplicates
#         return queryset.distinct()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context['title'] = 'Documents'
#         context['filter_pre'] = common.filter_pre
#         context['filter_pre_gt'] = common.filter_pre_gt
#         context['filter_pre_lt'] = common.filter_pre_lt
#         context['list_type'] = 'text'

#         # Options: Sort By
#         context['options_sortby'] = [
#             # Alphabetical
#             {
#                 'value': 'shelfmark__name',
#                 'label': 'Shelfmark'
#             },
#             # Numerical
#             {
#                 'value': f'{common.sort_pre_count_value}itemimage',
#                 'label': f'{common.sort_pre_count_label}Document Images'
#             },
#         ]

#         # Options: Filters
#         context['options_filters'] = [

#             # General
#             [
#                 {
#                     'filter_id': f'{common.filter_pre_mm}keywords',
#                     'filter_name': 'Keyword',
#                     'filter_options': models.SlKeyword.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}shelfmark',
#                     'filter_name': 'Shelfmark',
#                     'filter_options': models.SlDocumentShelfmark.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}category',
#                     'filter_name': 'Document Category',
#                     'filter_options': models.SlDocumentCategory.objects.all()
#                 },
#             ],

#             # Codicological/Document definition
#             [
#                 {
#                     'filter_id': f'{common.filter_pre_fk}format',
#                     'filter_name': 'Document Format',
#                     'filter_options': models.SlDocumentFormat.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}type_of_manuscript',
#                     'filter_name': 'Type of Manuscript',
#                     'filter_options': models.SlDocumentTypeOfManuscript.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}document_definition',
#                     'filter_name': 'Document Definition',
#                     'filter_options': models.SlDocumentDocumentDefinition.objects.all()
#                 },
#             ],

#             # Date
#             [
#                 {
#                     'filter_id': f'{common.filter_pre_gt}date_century__century_number',
#                     'filter_classes': common.filter_pre_gt,
#                     'filter_name': 'Date (from)',
#                     'filter_options': models.SlDateCentury.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_lt}date_century__century_number',
#                     'filter_classes': common.filter_pre_lt,
#                     'filter_name': 'Date (to)',
#                     'filter_options': models.SlDateCentury.objects.all()
#                 }
#             ],

#             # Document: Location & Language
#             [
#                 {
#                     'filter_id': f'{common.filter_pre_mm}estimated_geographical_areas',
#                     'filter_name': 'Estimated Geographical Area',
#                     'filter_options': models.SlDocumentEstimatedGeographicalArea.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_mm}languages',
#                     'filter_name': 'Language',
#                     'filter_options': models.SlDocumentLanguage.objects.all()
#                 }
#             ],

#             # Country > Town > Library
#             [
#                 {
#                     'filter_id': f'{common.filter_pre_fk}library__town__country',
#                     'filter_name': 'Repository Country',
#                     'filter_options': models.SlCountry.objects.all(),
#                     # Data hierarchy properties
#                     'data_hierarchy_id': 'country',
#                     'data_hierarchy_children': 'town library'
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}library__town',
#                     'filter_name': 'Repository Town/City',
#                     'filter_options': models.SlTown.objects.all().select_related('country'),
#                     # Data hierarchy properties
#                     'data_hierarchy_id': 'town',
#                     'data_hierarchy_children': 'library',
#                     'data_hierarchy_parents': 'country'
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}library',
#                     'filter_name': 'Library',
#                     'filter_options': models.SlLibrary.objects.all().select_related('town__country'),
#                     # Data hierarchy properties
#                     'data_hierarchy_id': 'library',
#                     'data_hierarchy_parents': 'country town'
#                 }
#             ]
#         ]

#         return context
