# from django.views.generic import (DetailView, ListView)
# from django.urls import reverse
# from .. import models
# from . import common


# class ItemDetailView(DetailView):
#     """
#     Class-based view for item detail template
#     """
#     template_name = 'palaeography/detail.html'
#     model = models.Item

#     def get_queryset(self):
#         return common.filter_by_user_role_permissions_view(self, self.model.objects.all())

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Admin URL
#         context['admin_url'] = reverse('admin:palaeography_item_change', args=[self.object.id])

#         # Details
#         context['details'] = common.details_section_visibility([
#             [
#                 # General
#                 {'label': 'Shelfmark', 'value': self.object.shelfmark},
#                 {'label': 'Name', 'value': self.object.name},
#                 {'label': 'Library', 'value': self.object.library}
#             ],
#             [
#                 # Codicological/Document Definition
#                 {'section_title': 'Codicological/Document Definition'},
#                 {'label': "Codicological Definition", 'value': self.object.codicological_definition},
#                 {'label': "Format", 'value': self.object.format},
#                 {'label': "Format (Other)", 'value': self.object.format_other},
#                 {'label': "Type Of Manuscript", 'value': self.object.type_of_manuscript},
#                 {'label': "Codicological Definition Observations", 'value': self.object.codicological_definition_observations},
#                 {'label': "Document Definition", 'value': self.object.document_definition},
#                 {'label': "Document Definition Observations", 'value': self.object.document_definition_observations},
#                 ],
#             [
#                 # Content Description
#                 {'section_title': 'Content Description'},
#                 {'label': "Subject Fields", 'value': common.html_details_list_items(self.object.subject_fields.all())},
#                 {'label': "Fields", 'value': common.html_details_list_items(self.object.fields.all())},
#                 {'label': "Fields (Other)", 'value': self.object.fields_other},
#                 {'label': "Fields Observations", 'value': self.object.fields_observations},
#                 {'label': "Languages", 'value': common.html_details_list_items(self.object.languages.all())},
#                 {'label': "Languages Observations", 'value': self.object.languages_observations},
#                 {'label': "Edition", 'value': self.object.edition},
#                 {'label': "Translation", 'value': self.object.translation},
#                 {'label': "Keywords", 'value': common.html_details_list_items(self.object.keywords.all())},
#                 {'label': "Keywords Observations", 'value': self.object.keywords_observations},
#                 {'label': "Author Name In Manuscript", 'value': self.object.author_name_in_manuscript},
#                 {'label': "Author Uniform Name", 'value': self.object.author_uniform_name},
#                 {'label': "Author's Dates And Places", 'value': self.object.author_dates_and_places},
#                 {'label': "Author Observations", 'value': self.object.author_observations},
#                 {'label': "Title In Manuscript", 'value': self.object.title_in_manuscript},
#                 {'label': "Uniform Title", 'value': self.object.uniform_title},
#                 {'label': "Title Observations", 'value': self.object.title_observations},
#                 {'label': "Text Description", 'value': self.object.text},
#                 {'label': "Incipit", 'value': self.object.incipit},
#                 {'label': "Explicit", 'value': self.object.explicit},
#                 {'label': "Section Titles", 'value': self.object.section_titles},
#                 {'label': "Date Mentioned", 'value': self.object.date_mentioned},
#                 {'label': "Date Ce", 'value': self.object.date_ce},
#                 {'label': "Date Century", 'value': self.object.date_century},
#                 {'label': "Date Observations", 'value': self.object.date_observations},
#                 {'label': "Locality Of Writing", 'value': self.object.locality_of_writing},
#                 {'label': "Locality Mentioned", 'value': self.object.locality_mentioned},
#                 {'label': "Estimated Geographical Areas", 'value': common.html_details_list_items(self.object.estimated_geographical_areas.all())},
#                 {'label': "Estimated Locality", 'value': self.object.estimated_locality},
#                 {'label': "Locality Observations", 'value': self.object.locality_observations},
#                 {'label': "Incodicated Document Observations", 'value': self.object.incodicated_documents_observations},
#                 {'label': "Historical Information", 'value': common.html_details_list_items(self.object.historical_informations.all())},
#                 {'label': "Paratext", 'value': common.html_details_list_items(self.object.paratexts.all())},
#                 ],
#             [
#                 # Physical Description
#                 {'section_title': 'Physical Description'},
#                 {'label': "Height", 'value': self.object.height},
#                 {'label': "Width", 'value': self.object.width},
#                 {'label': "Height Of Written Area", 'value': self.object.height_of_written_area},
#                 {'label': "Width Of Written Area", 'value': self.object.width_of_written_area},
#                 {'label': "Height Of Outer Cover", 'value': self.object.height_of_outer_cover},
#                 {'label': "Width Of Outer Cover", 'value': self.object.width_of_outer_cover},
#                 {'label': "Dimensions Observations", 'value': self.object.dimensions_observations},
#                 {'label': "Number Of Folios", 'value': self.object.number_of_folios},
#                 {'label': "State Of The Item", 'value': self.object.state_of_item},
#                 {'label': "State Of Item Observations", 'value': self.object.state_of_item_observations},
#                 {'label': "State Of Material", 'value': self.object.state_of_material},
#                 {'label': "State Of Writing", 'value': self.object.state_of_writing},
#                 {'label': "State Of Writing Observations", 'value': self.object.state_of_writing_observations},
#                 {'label': "Palimpsest", 'value': self.object.palimpsest},
#                 {'label': "Palimpsest Underscript", 'value': self.object.palimpsest_underscript},
#                 {'label': "Writing Materials", 'value': common.html_details_list_items(self.object.writing_materials.all())},
#                 {'label': "Paper", 'value': common.html_details_list_items(self.object.papers.all())},
#                 {'label': "Writing Materials Colour", 'value': self.object.writing_materials_colour},
#                 {'label': "Writing Materials Thickness", 'value': self.object.writing_materials_thickness},
#                 {'label': "Writing Materials Translucency", 'value': self.object.writing_materials_translucency},
#                 {'label': "Writing Materials Observations", 'value': self.object.writing_materials_observations},
#                 {'label': "Inks", 'value': common.html_details_list_items(self.object.inks.all())},
#                 {'label': "Inks Observations", 'value': self.object.inks_observations},
#                 {'label': "Formula For The Quires", 'value': self.object.formula_for_the_quires},
#                 {'label': "Parchment Quires, Hair/Flesh Distribution", 'value': self.object.parchment_quires_hair_or_flesh_distribution},
#                 {'label': "Ordering The Quires", 'value': common.html_details_list_items(self.object.ordering_quires.all())},
#                 {'label': "Quires Observations", 'value': self.object.quires_observations},
#                 {'label': "Pricking", 'value': self.object.pricking},
#                 {'label': "Pricking Instrument", 'value': self.object.pricking_instrument},
#                 {'label': "Pricking Pattern", 'value': self.object.pricking_pattern},
#                 {'label': "Pricking Observations", 'value': self.object.pricking_observations},
#                 {'label': "Ruling", 'value': self.object.ruling},
#                 {'label': "Ruling Method", 'value': self.object.ruling_method},
#                 {'label': "Ruling Pattern", 'value': self.object.ruling_pattern},
#                 {'label': "Number Of Ruled Lines", 'value': self.object.number_of_ruled_lines},
#                 {'label': "Ruling Observations", 'value': self.object.ruling_observations},
#                 {'label': "Page Layouts", 'value': common.html_details_list_items(self.object.page_layouts.all())},
#                 {'label': "Columns, Number Per Page/Sheet", 'value': self.object.number_of_collumns_per_page_or_sheet},
#                 {'label': "Cul-De-Lampe", 'value': self.object.cul_de_lampe},
#                 {'label': "Tables", 'value': self.object.tables},
#                 {'label': "Number Of Leaves", 'value': self.object.number_of_leaves},
#                 {'label': "Number Of Written Lines", 'value': self.object.number_of_written_lines},
#                 {'label': "Justifications", 'value': common.html_details_list_items(self.object.justifications.all())},
#                 {'label': "Justifications Other", 'value': self.object.justifications_other},
#                 {'label': "Justifications Observations", 'value': self.object.justifications_observations},
#                 {'label': "Text Layouts", 'value': common.html_details_list_items(self.object.text_layouts.all())},
#                 {'label': "Paragraph Marks And Textual Dividers", 'value': self.object.paragraph_marks_and_textual_dividers},
#                 {'label': "Text Layouts (Other)", 'value': self.object.text_layouts_other},
#                 {'label': "Text Layouts Observations", 'value': self.object.text_layouts_observations},
#                 {'label': "Graphic Systems (Script)", 'value': common.html_details_list_items(self.object.graphic_systems.all())},
#                 {'label': "Script Type", 'value': self.object.script_type},
#                 {'label': "Script Mode", 'value': self.object.script_mode},
#                 {'label': "Script Quality", 'value': self.object.script_quality},
#                 {'label': "Script Function", 'value': self.object.script_function},
#                 {'label': "Script Function (Other)", 'value': self.object.script_function_other},
#                 {'label': "Script Style", 'value': self.object.script_style},
#                 {'label': "Script Style (Other)", 'value': self.object.script_style_other},
#                 {'label': "Script Observations", 'value': self.object.script_observations},
#                 {'label': "Number Of Hands", 'value': self.object.number_of_hands},
#                 {'label': "Hands", 'value': common.html_details_list_items(self.object.hands.all())},
#                 {'label': "Vocalization", 'value': self.object.vocalization},
#                 {'label': "Vocalization Types", 'value': common.html_details_list_items(self.object.vocalization_types.all())},
#                 {'label': "Vocalization Observations", 'value': self.object.vocalization_observations},
#                 {'label': "Names Of God", 'value': common.html_details_list_items(self.object.names_of_god.all())},
#                 {'label': "Abbreviations", 'value': self.object.abbreviations},
#                 {'label': "Special Signs For Vernacular Words In Hebrew Letters", 'value': self.object.special_signs_for_vernacular_words},
#                 {'label': "Judeo-Arabic Diacritics", 'value': common.html_details_list_items(self.object.judeo_arabic_diacritics.all())},
#                 {'label': "Invocation", 'value': self.object.invocation},
#                 {'label': "Invocation (Other)", 'value': self.object.invocation_other},
#                 {'label': "Graphic Signs Observations", 'value': self.object.graphic_signs_observations},
#                 {'label': "Decorations", 'value': common.html_details_list_items(self.object.decorations.all())},
#                 {'label': "Decorations Observations", 'value': self.object.decorations_observations},
#                 {'label': "Glosses", 'value': common.html_details_list_items(self.object.glosses.all())},
#                 {'label': "Glosses Observations", 'value': self.object.glosses_observations},
#                 {'label': "Binding", 'value': self.object.binding},
#                 {'label': "Binding Materials", 'value': self.object.binding_materials},
#                 {'label': "Binding Type", 'value': self.object.binding_type},
#                 {'label': "Outer Cover Decoration", 'value': self.object.outer_cover_decoration},
#                 {'label': "Inner Cover", 'value': self.object.inner_cover},
#                 {'label': "Endbands", 'value': self.object.endbands},
#                 {'label': "Spine", 'value': self.object.spine},
#                 {'label': "Sewing", 'value': self.object.sewing},
#                 {'label': "Number Of Sewing Stations", 'value': self.object.number_of_sewing_stations},
#                 {'label': "Thread", 'value': self.object.thread},
#                 {'label': "Type Of Sewing", 'value': self.object.type_of_sewing},
#                 {'label': "Binding Observations", 'value': self.object.binding_observations},
#             ],
#             [
#                 # Miscellaneous
#                 {'section_title': 'Miscellaneous'},
#                 {'label': "Manuscript History", 'value': self.object.manuscript_history},
#                 {'label': "Bibliography", 'value': self.object.bibliography},
#             ]
#         ])

#         # Related data
#         context['related_data_list'] = [
#             {
#                 'title': 'Item Images',
#                 'id': 'itemimages',
#                 'list_type': 'image',
#                 'objects': common.filter_by_user_role_permissions_view(self, self.object.itemimages)
#             },
#             {
#                 'title': 'Other Items in Shelfmark',
#                 'id': 'otheritemsinshelfmark',
#                 'list_type': 'text',
#                 'objects': common.filter_by_user_role_permissions_view(
#                     self,
#                     models.Item.objects.filter(
#                         admin_published=True,
#                         shelfmark=self.object.shelfmark).exclude(id=self.object.id)
#                 )
#             },
#         ]

#         return context


# class ItemListView(ListView):
#     """
#     Class-based view for item list template
#     """
#     template_name = 'palaeography/list.html'
#     model = models.Item
#     paginate_by = common.PAGINATE_COUNT

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

#         context['title'] = 'Items'
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
#                 'label': f'{common.sort_pre_count_label}Item Images'
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
#                     'filter_options': models.SlItemShelfmark.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}category',
#                     'filter_name': 'Item Category',
#                     'filter_options': models.SlItemCategory.objects.all()
#                 },
#             ],

#             # Codicological/Document definition
#             [
#                 {
#                     'filter_id': f'{common.filter_pre_fk}format',
#                     'filter_name': 'Item Format',
#                     'filter_options': models.SlItemFormat.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}type_of_manuscript',
#                     'filter_name': 'Type of Manuscript',
#                     'filter_options': models.SlItemTypeOfManuscript.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_fk}document_definition',
#                     'filter_name': 'Document Definition',
#                     'filter_options': models.SlItemDocumentDefinition.objects.all()
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

#             # Item: Location & Language
#             [
#                 {
#                     'filter_id': f'{common.filter_pre_mm}estimated_geographical_areas',
#                     'filter_name': 'Estimated Geographical Area',
#                     'filter_options': models.SlItemEstimatedGeographicalArea.objects.all()
#                 },
#                 {
#                     'filter_id': f'{common.filter_pre_mm}languages',
#                     'filter_name': 'Language',
#                     'filter_options': models.SlItemLanguage.objects.all()
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
