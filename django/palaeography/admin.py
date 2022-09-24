from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from . import models
from .apps import app_name


admin.site.site_header = 'MultiPal: Dashboard'


def publish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to published
    """
    for object in queryset:
        object.admin_published = True
        # Set first published datetime, if applicable
        try:
            if object.meta_firstpublished_datetime is None:
                object.meta_firstpublished_datetime = timezone.now()
        except Exception:
            pass
        object.save()


publish.short_description = "Publish selected objects (will appear on main site)"


def unpublish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to not published
    """
    for object in queryset:
        object.admin_published = True
        object.save()


unpublish.short_description = "Unpublish selected objects (will not appear on main site)"


def fk_link(object, fk_field):
    """
    Generate a link for foreign key fields in admin lists
    """
    try:
        fk = getattr(object, fk_field)  # get the foreign key object
        model_name = fk.__class__.__name__.lower().replace('_', '')
        url = reverse(f"admin:{app_name}_{model_name}_change", args=[fk.id])
        return mark_safe(f'<a href="{url}">{fk}</a>')
    except AttributeError:
        return "-"  # If FK value is null


def get_model_perms_dict(self, request):
    """
    This is the default get_model_perms permissions dictionary

    The method `get_model_perms(): return {}` is used to hide select list models from admin side bar

    However, some SL models need to be shown, so returning the following line to these ModelAdmins:
    `get_model_perms(): return get_model_perms_dict(self, request)`
    (which uses this function) will show these select list models in the sidebar
    """
    return {
        'add': self.has_add_permission(request),
        'change': self.has_change_permission(request),
        'delete': self.has_delete_permission(request),
        'view': self.has_view_permission(request)
    }


def custom_permission(self, request):
    """
    If specific, custom permissions are needed (e.g. user can only change/delete their own object)
    then call this function via the following methods on a ModelAdmin below:
    - has_change_permission(self, request, obj=None)
    - has_delete_permission(self, request, obj=None)

    self = the ModelAdmin class (or inherited class), which calls this during a method
    request = the request in the ModelAdmin, which contains info about user, path, etc.
    """
    path = request.path.split('/')  # path example: '/dashboard/palaeography/item/1/change/'

    # Ensure it only checks for the current model, as specified in request path,
    # as (for some reason) it triggers multiple times for other models, causing errors
    if len(path) > 3 and self.model._meta.model_name == path[3]:
        # If an object is being changed or deleted, as specified in request path
        if path[-2] in ['change', 'delete']:
            # Admins can change/delete all
            if request.user.role.name == 'admin':
                return True
            # Collaborators can change/delete if it's their own (i.e. if they created it)
            elif request.user.role.name == 'collaborator' and self.model.objects.get(id=int(path[-3])).meta_created_by == request.user:
                return True
        return False  # Deny access if no above condition has been met


class GenericAdminView(admin.ModelAdmin):
    """
    This is a generic class that can be applied to most models to customise their inclusion in the Django admin.

    This class can either be inherited from to customise, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if you don't need to customise it just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """
    list_display = ('name', 'admin_published', 'meta_created_datetime', 'meta_lastupdated_datetime')
    list_display_links = ('name',)
    list_filter = ('admin_published', 'meta_created_by')
    search_fields = ('name', 'admin_notes')
    actions = (publish, unpublish)
    readonly_fields = ['admin_published',
                       'meta_created_by',
                       'meta_created_datetime',
                       'meta_lastupdated_by',
                       'meta_lastupdated_datetime',
                       'meta_firstpublished_datetime']

    def get_actions(self, request):
        actions = super().get_actions(request)

        # Collaborators can't publish/unpublish objects
        if request.user.role.name == 'collaborator':
            del actions['publish']
            del actions['unpublish']

        return actions

    def save_model(self, request, obj, form, change):
        # Meta: created (if not yet set) or last updated by (if created already set)
        if obj.meta_created_by is None:
            obj.meta_created_by = request.user
            # meta_created_datetime default value set in model so not needed here
        else:
            obj.meta_lastupdated_by = request.user
            obj.meta_lastupdated_datetime = timezone.now()
        # Meta: first published datetime
        if obj.admin_published and obj.meta_firstpublished_datetime is None:
            obj.meta_firstpublished_datetime = timezone.now()
        obj.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        try:
            # Meta: contributors
            form.instance.meta_contributors.add(request.user)
        except Exception:
            pass

    def has_change_permission(self, request, obj=None):
        return custom_permission(self, request)

    def has_delete_permission(self, request, obj=None):
        return custom_permission(self, request)


class GenericSlAdminView(admin.ModelAdmin):
    """
    This is a generic base class that can be inherited from by Select List models

    This class can either be inherited from if further customisations are needed, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if no changes are needed, just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

    def get_model_perms(self, request):
        """
        Hide SL tables from admin side bar, but still CRUD via inline shortcuts on main models
        Show SL tables for some users (as determined by USERS_CAN_MANAGE_SELECT_LISTS_IN_DASHBOARD in local_settings.py)
        """
        if request.user.email in settings.USERS_CAN_MANAGE_SELECT_LISTS_IN_DASHBOARD:
            return admin.ModelAdmin.get_model_perms(self, request)
        else:
            return {}

    def has_change_permission(self, request, obj=None):
        return custom_permission(self, request)

    def has_delete_permission(self, request, obj=None):
        return custom_permission(self, request)


# Inlines


# class GenericStackedInline(admin.StackedInline):
#     """A generic stacked inline with common settings to be used by actual inlines below"""
#     extra = 0
#     classes = ['collapse']


# class GenericTabularInline(admin.TabularInline):
#     """A generic tabular inline with common settings to be used by actual inlines below"""
#     extra = 0
#     classes = ['collapse']


# class ItemHandInline(GenericStackedInline):
#     """A subform/inline form for ItemHand to be used in ItemAdmin"""
#     model = models.ItemHand




# Admin views for main models


# class ItemAdminView(GenericAdminView):
#     """Customise the admin interface for Item model"""
#     list_display = ('shelfmark',
#                     'name',
#                     'library',
#                     'category',
#                     'number_of_hands',
#                     'admin_published',
#                     'meta_created_by',
#                     'meta_created_datetime',
#                     'meta_lastupdated_by',
#                     'meta_lastupdated_datetime')
#     list_select_related = ('library__town__country',
#                            'category',
#                            'meta_created_by',
#                            'meta_lastupdated_by')
#     list_display_links = ('shelfmark',)
#     list_filter = ('admin_published', 'category', 'languages')
#     search_fields = models.search_fields_item
#     filter_horizontal = ('subject_fields',)
#     inlines = (
#         ItemHandInline,
#         ItemHistoricalInformationInline,
#         ItemJudeoArabicDiacriticsInline,
#         ItemOrderingQuiresInline,
#         ItemPaperInline,
#         ItemParatextInline
#     )
#     autocomplete_fields = ('library',
#                            'codicological_definition',
#                            'format',
#                            'type_of_manuscript',
#                            'document_definition',
#                            'state_of_item',
#                            'state_of_material',
#                            'state_of_writing',
#                            'palimpsest',
#                            'pricking',
#                            'pricking_instrument',
#                            'pricking_pattern',
#                            'ruling',
#                            'ruling_method',
#                            'ruling_pattern',
#                            'script_type',
#                            'script_mode',
#                            'script_quality',
#                            'script_function',
#                            'script_style',
#                            'vocalization',
#                            'abbreviations',
#                            'invocation',
#                            'binding',
#                            'type_of_sewing')
#     fieldsets = (
#         ('General', {
#             'fields': (
#                 'shelfmark',
#                 'name',
#                 'library',
#                 'category',
#                 'description',
#                 'keywords',
#                 'keywords_observations'
#             )
#         }),
#         ('Codicological/Document definition', {
#             'fields': (
#                 'codicological_definition',
#                 'document_definition',
#                 ('format', 'format_other'),
#                 'type_of_manuscript',
#                 'codicological_definition_observations',
#                 'document_definition_observations',
#             )
#         }),
#         ('Content Description', {
#             'fields': (
#                 'subject_fields',
#                 ('fields', 'fields_other'),
#                 'fields_observations',
#                 'languages', 'languages_observations',
#                 'edition',
#                 'translation',
#                 ('author_name_in_manuscript', 'author_uniform_name', 'author_dates_and_places'),
#                 'author_observations',
#                 'title_in_manuscript',
#                 'uniform_title',
#                 'title_observations',
#                 'incipit',
#                 'explicit',
#                 'section_titles',
#                 'date_mentioned',
#                 'date_ce',
#                 'date_century',
#                 'date_observations',
#                 'locality_of_writing',
#                 'locality_mentioned',
#                 'estimated_geographical_areas',
#                 'estimated_locality',
#                 'locality_observations',
#                 'incodicated_documents_observations',
#                 # Historical Information inline here via JS
#                 # Paratext inline here via JS
#             )
#         }),
#         ('Physical Description', {
#             'fields': (
#                 ('height', 'width'),
#                 ('height_of_written_area', 'width_of_written_area'),
#                 ('height_of_outer_cover', 'width_of_outer_cover'),
#                 'dimensions_observations',
#                 'number_of_folios',
#                 'state_of_item',
#                 'state_of_item_observations',
#                 'state_of_material',
#                 'state_of_material_observations',
#                 'state_of_writing',
#                 'state_of_writing_observations',
#                 'palimpsest',
#                 'palimpsest_underscript',
#                 'writing_materials',
#                 # Paper inline here via JS
#                 'writing_materials_colour',
#                 'writing_materials_thickness',
#                 'writing_materials_translucency',
#                 'writing_materials_observations',
#                 'inks',
#                 'inks_observations',
#                 'formula_for_the_quires',
#                 'parchment_quires_hair_or_flesh_distribution',
#                 # Ordering Quires inline here via JS
#                 'quires_observations',
#                 'pricking',
#                 'pricking_instrument',
#                 'pricking_pattern',
#                 'pricking_observations',
#                 'ruling',
#                 'ruling_method',
#                 'ruling_pattern',
#                 'number_of_ruled_lines',
#                 'ruling_observations',
#                 'page_layouts',
#                 'number_of_collumns_per_page_or_sheet',
#                 'cul_de_lampe',
#                 'tables',
#                 'number_of_leaves',
#                 'number_of_written_lines',
#                 ('justifications', 'justifications_other'),
#                 'justifications_observations',
#                 'text_layouts',
#                 'paragraph_marks_and_textual_dividers',
#                 'text_layouts_other',
#                 'text_layouts_observations',
#                 'graphic_systems',
#                 'script_type',
#                 'script_mode',
#                 'script_quality',
#                 ('script_function', 'script_function_other'),
#                 ('script_style', 'script_style_other'),
#                 'script_observations',
#                 'number_of_hands',
#                 # Hands inline here via JS
#                 'vocalization',
#                 'vocalization_types',
#                 'vocalization_observations',
#                 'names_of_god',
#                 'abbreviations',
#                 # Judeo-Arabic Diacritics inline here via JS
#                 'special_signs_for_vernacular_words',
#                 ('invocation', 'invocation_other'),
#                 'graphic_signs_observations',
#                 'decorations',
#                 'decorations_observations',
#                 'glosses',
#                 'glosses_observations',
#                 'binding',
#                 'binding_materials',
#                 'binding_type',
#                 'outer_cover_decoration',
#                 'inner_cover',
#                 'endbands',
#                 'spine',
#                 'sewing',
#                 'number_of_sewing_stations',
#                 'thread',
#                 'type_of_sewing',
#                 'binding_observations',
#             )
#         }),
#         ('Miscellaneous', {
#             'fields': (
#                 'manuscript_history',
#                 'bibliography'
#             )
#         }),
#         ('Admin', {
#             'fields': (
#                 'admin_published',
#                 'admin_notes',
#                 'meta_editors',
#                 'meta_contributors',
#                 'meta_created_by',
#                 'meta_created_datetime',
#                 'meta_lastupdated_by',
#                 'meta_lastupdated_datetime',
#                 'meta_firstpublished_datetime',
#             )
#         }),
#     )

#     class Media:
#         # This AdminView requires custom JS (which uses jQuery)
#         js = (
#             'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
#             'js/admin_item.js'
#         )


# class ItemImageAdminView(GenericAdminView):
#     """Customise the admin interface for ItemImage model"""
#     list_display = ('name',
#                     'image',
#                     'category',
#                     'admin_published',
#                     'meta_created_by',
#                     'meta_created_datetime',
#                     'meta_lastupdated_by',
#                     'meta_lastupdated_datetime')
#     list_select_related = ('item',
#                            'category',
#                            'meta_created_by',
#                            'meta_lastupdated_by')
#     list_filter = ('admin_published', 'category', 'item__category', 'item__languages')
#     search_fields = models.search_fields_itemimage
#     autocomplete_fields = ('item',)
#     exclude = ('image_original', 'image_thumbnail')


# Register admin views

# Main tables
# admin.site.register(models.Item, ItemAdminView)
# admin.site.register(models.ItemImage, ItemImageAdminView)
