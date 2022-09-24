"""
This script is for common resources (e.g. functions) used throughout the main views
"""

from django.db.models.functions import Lower
from django.db.models import (Count, Q, CharField, TextField)
from functools import reduce
from operator import (or_, and_)
from .. import models
import json


PAGINATE_COUNT = 64  # specified here to establish same pagination count throughout all views


def html_anchor_tag(self, object, label=None, url_parameters=''):
    """
    Returns a HTML anchor tag <a href="...">...</a> for a given object
    The object must have a valid 'url_detail' dynamic property in its model

    Optional label, otherwise object __str__ will be used as the label

    Optional url parameters can be passed, e.g. tab=image in www.myurl.com?tab=image
    """

    # Add a ? to start of url_parameters, if ? not already included
    url_parameters = f'?{url_parameters}' if len(url_parameters) > 1 and url_parameters[0] != '?' else url_parameters

    # If object exists
    if object:
        # Return an anchor link if user has permission to view linked object
        if object in filter_by_user_role_permissions_view(self, object.__class__.objects.all()):
            return f'<a href="{object.url_detail}{url_parameters}">{label if label else object}</a>'
        # If user doesn't have permission to view linked object, just show its name as text
        else:
            return f'<span>{label if label else object}</span>'
    # If object doesn't exist
    else:
        return False


def html_details_list_items(object_list):
    """
    Return a HTML string of a list of objects (i.e. a queryset) for use in the 'Details' tab of an item page.
    E.g. showing ManyToMany and reverse FK objects

    The model of the object_list must have a dynamic property 'html_details_list_item_text'
    """

    # Multiple objects
    if len(object_list) > 1:
        list_items = '</li><li>'.join(str(item.html_details_list_item_text) for item in object_list)
        return f'<ul><li>{list_items}</li></ul>'
    # 1 object
    elif len(object_list) == 1:
        return str(object_list[0].html_details_list_item_text)
    # No objects (will be ignored)
    else:
        return ""


def details_section_visibility(details_list):
    """
    Show the detail section if at least one value exists
    """
    for section in details_list:
        if len(section):
            for detail in section:
                if 'value' in detail and detail['value']:
                    section[0]['section_visible'] = True
                    break
    return details_list


def set_metadata(obj, request):
    """
    Set metadata fields that need the user info, e.g. Created By
    """
    # Meta: created by
    if getattr(obj, 'meta_created_by', None) is None:
        obj.meta_created_by = request.user
    # Meta: last updated by
        obj.meta_lastupdated_by = request.user
    # Save
    obj.save()


def get_field_type(field_name, queryset):
    """
    Return the type of a field
    E.g. used in sort() to see if case insensitivity is needed (if field is a CharField/TextField)
    """
    try:
        stripped_field_name = field_name.lstrip('-')
        if stripped_field_name in queryset.query.annotations:
            return queryset.query.annotations[stripped_field_name].output_field
        return queryset.model._meta.get_field(stripped_field_name)
    except Exception:
        return CharField  # If it fails, assume it's a CharField by default


def filter_by_user_role_permissions_view(self, queryset):
    """
    self = self from the view calling this function
    queryset = queryset to be filtered

    Return a filtered queryset containing objects the current user can VIEW based on permissions of their role:
    - Admins: view all objects
    - Collaborator: show all published objects and objects created by current user
    - General users (no account): show published objects only
    """

    # Admin (don't filter, return original queryset)
    if self.request.user.is_authenticated and self.request.user.role.name == 'admin':
        return queryset

    # If not an admin (i.e. not logged in or a collaborator) then must filter further (e.g. based on admin_published, etc.)
    else:
        # Build initial query
        query = Q(admin_published=True)

        # Add to query, based on model of current queryset
        # Certain models are dependent on parent object's admin_published status
        # E.g. if an ItemImage is published but its parent Item is not, then it shouldn't show as it's parent isn't published

        # ItemImage
        if queryset.model is models.ItemImage:
            query.add(Q(item__admin_published=True), Q.AND)
        # WorkQuotation
        elif queryset.model is models.WorkQuotation:
            query.add(Q(work__admin_published=True), Q.AND)

        # Add to query, based on user's role

        # Collaborator
        if self.request.user.is_authenticated and self.request.user.role.name == 'collaborator':
            # Collaborators can see all content that they created
            query.add(Q(meta_created_by=self.request.user), Q.OR)

        # Use finished query to filter queryset
        return queryset.filter(query)


def user_can_edit_object(self, object):
    """
    self = self from the view calling this function
    object = a Django model object

    Return True if the current user has permission to EDIT specified object:
    - Admins: edit all objects
    - Collaborator: edit objects created by current user
    - General users (no account): cannot edit any
    """

    # Admin (don't filter, return original queryset)
    if self.request.user.is_authenticated and self.request.user.role.name == 'admin':
        return True

    # Collaborator
    elif self.request.user.is_authenticated and self.request.user.role.name == 'collaborator':
        return True if object.meta_created_by == self.request.user else False

    # General users (no account)
    elif not self.request.user.is_authenticated:
        return False


def search(request, queryset, field_names_to_search):
    """
    request = http request object, e.g. self.request
    queryset = the Django queryset to be searched
    field_names_to_search = list of names of the fields to include in search

    Returns a filtered/searched Django queryset, allowing for multiple search criteria and operator (or_ / and_)
    """

    # Search
    searches = json.loads(request.GET.get('search', '[]'))

    # Set list of search options
    if searches not in [[''], []]:
        operator = or_ if request.GET.get('search_operator', '') == 'or' else and_
        queries = []
        for search in searches:
            # Uses 'or_' as the search term could appear in any field, so 'and_' wouldn't be suitable
            queries.append(reduce(or_, (Q((f'{field_name}__icontains', search)) for field_name in field_names_to_search)))
        # Connect the individual search queries via the user-defined operator (or_ / and_)
        queries = reduce(operator, queries)
        # Filter the queryset using the completed search query
        return queryset.filter(queries)

    # If no search criteria provided, simply return the unfiltered queryset
    return queryset


# Special starts to the values & labels of options in 'filter' select lists, used in below filter() function and within views scripts
filter_pre = 'filter_'
filter_pre_mm = f'{filter_pre}mm_'  # Many to Many relationship
filter_pre_fk = f'{filter_pre}fk_'  # Foreign Key relationship
filter_pre_gt = f'{filter_pre}gt_'  # Greater than (or equal to) filter, e.g. "Date (from)"
filter_pre_lt = f'{filter_pre}lt_'  # Less than (or equal to) filter, e.g. "Date (to)"


def filter(request, queryset):
    """
    request = http request object, e.g. self.request
    queryset = the Django queryset to be searched

    Returns a filtered Django queryset, allowing for multiple filters (of M2M and FK relationships) to be applied
    """

    # Only loop through filter values in all GET request values (e.g. exclude search, sort, etc. values)
    for filter_key in [k for k in list(request.GET.keys()) if k.startswith(filter_pre)]:

        filter_value = request.GET.get(filter_key, '')
        if filter_value != '':

            # Many to Many relationship (uses __in comparison and filter_value is a list)
            if filter_key.startswith(filter_pre_mm):
                filter_field = filter_key.replace(filter_pre_mm, '')
                queryset = queryset.filter(**{f'{filter_field}__in': [filter_value]})

            # Foreign Key relationship
            elif filter_key.startswith(filter_pre_fk):
                filter_field = filter_key.replace(filter_pre_fk, '')
                queryset = queryset.filter(**{filter_field: filter_value})

            # Greater than or equal to
            elif filter_key.startswith(filter_pre_gt):
                filter_field = filter_key.replace(filter_pre_gt, '')
                queryset = queryset.filter(**{f'{filter_field}__gte': filter_value})

            # Less than or equal to
            elif filter_key.startswith(filter_pre_lt):
                filter_field = filter_key.replace(filter_pre_lt, '')
                queryset = queryset.filter(**{f'{filter_field}__lte': filter_value})

    return queryset


# Special starts to the values & labels of options in 'sort by' select lists, used in below sort() function and within views scripts
sort_pre_count_value = 'count_'
sort_pre_count_label = 'Number of '


def sort(request, queryset, sort_by_default='id'):
    """
    request = http request object, e.g. self.request
    queryset = the Django queryset to be sorted
    sort_by_default = default field to sort by, e.g. name, id, ...

    Returns a sorted Django queryset
    """

    # Establish the sort direction (asc/desc) and the field to sort by, from the request
    sort_dir = request.GET.get('sort_direction', '')
    sort_by = request.GET.get('sort_by', sort_by_default)
    sort = sort_dir + sort_by
    sort_pre_length = len(f"{sort_dir}{sort_pre_count_value}")  # e.g. '-count_' for descending numerical

    # Count sorting (e.g. sort by count of related items)
    if sort_pre_count_value in sort:
        order_by = sort_dir + 'countitems'  # '-countitems' if descending, 'countitems' if ascending
        # Try to apply the admin_published=True constraint
        sort_field = sort[sort_pre_length:]
        try:
            q_filter_admin_published = {sort_field + '__admin_published': True}
            return queryset.annotate(countitems=Count(sort_field, filter=Q(**q_filter_admin_published))).order_by(order_by)
        # When it fails, simply return the count without filtering
        except Exception:
            return queryset.annotate(countitems=Count(sort_field)).order_by(order_by)

    # Standard sort
    else:

        # Sort descending (Z-A)
        if sort_dir == '-':
            # Convert CharField and TextField values to lowercase, for case insensitivity
            if isinstance(get_field_type(sort, queryset), (CharField, TextField)):
                return queryset.order_by(Lower(sort[1:]).desc())
            else:
                return queryset.order_by(sort)

        # Sort ascending (A-Z)
        else:
            # Convert CharField and TextField values to lowercase, for case insensitivity
            if isinstance(get_field_type(sort, queryset), (CharField, TextField)):
                return queryset.order_by(Lower(sort))
            else:
                return queryset.order_by(sort)
