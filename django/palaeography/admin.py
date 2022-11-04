from django.contrib import admin
from django.db.models import ManyToManyField
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from . import models
from .apps import app_name


admin.site.site_header = 'MultiPal: Dashboard'


# Actions


def publish(modeladmin, request, queryset):
    # Sets all objects in queryset to: admin_published = True
    queryset.update(admin_published=True)


def unpublish(modeladmin, request, queryset):
    # Sets all objects in queryset to: admin_published = False
    queryset.update(admin_published=False)


publish.short_description = "Published (shown on public website)"
unpublish.short_description = "Unpublished (hidden from public website)"


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


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) == ManyToManyField and f.name not in exclude)


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
    readonly_fields = ['meta_created_by',
                       'meta_created_datetime',
                       'meta_lastupdated_by',
                       'meta_lastupdated_datetime']

    def save_model(self, request, obj, form, change):
        if obj.meta_created_by is None:
            obj.meta_created_by = request.user
        else:
            obj.meta_lastupdated_by = request.user
            obj.meta_lastupdated_datetime = timezone.now()
        obj.save()

    def has_delete_permission(self, request, obj=None):
        return False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)


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
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Inlines


class DocumentImageInline(admin.TabularInline):
    """A subform/inline form for DocumentHand to be used in DocumentAdmin"""
    model = models.DocumentImage
    extra = 1
    exclude = ('image_thumbnail',)
    readonly_fields = ('meta_created_datetime',
                       'meta_lastupdated_datetime')

    def save_model(self, request, obj, form, change):
        # Meta: created (if not yet set) or last updated by (if created already set)
        if obj.meta_created_by is None:
            obj.meta_created_by = request.user
            # meta_created_datetime default value set in model so not needed here
        else:
            obj.meta_lastupdated_by = request.user
            obj.meta_lastupdated_datetime = timezone.now()
        obj.save()


# Admin views for main models


class DocumentAdminView(GenericAdminView):
    """Customise the admin interface for Document model"""
    list_display = ('name',
                    'type',
                    'admin_published',
                    'meta_created_by',
                    'meta_created_datetime',
                    'meta_lastupdated_by',
                    'meta_lastupdated_datetime')
    inlines = (DocumentImageInline,)


# Register admin views

# Main tables
admin.site.register(models.Document, DocumentAdminView)

# Select list tables
admin.site.register(models.SlDocumentInk, GenericSlAdminView)
admin.site.register(models.SlDocumentLanguage, GenericSlAdminView)
admin.site.register(models.SlDocumentRepository, GenericSlAdminView)
admin.site.register(models.SlDocumentType, GenericSlAdminView)
