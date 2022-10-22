from django.views.generic import (DetailView, ListView)
from . import models


def help_queryset(self):
    """
    Applies required filtering for Help objects
    To be used in below get_queryset() methods
    """

    # Only ever show published objects
    queryset = self.model.objects.filter(admin_published=True)

    # If user is not an admin
    if not self.request.user.is_staff:
        # Hide help item marked as visible_only_to_admins
        queryset = queryset.exclude(visible_only_to_admins=True)

    return queryset


class HelpDetailView(DetailView):
    """
    Class-based view for help detail template
    """
    template_name = 'help/detail.html'
    model = models.HelpItem

    def get_queryset(self):
        return help_queryset(self)


class HelpListView(ListView):
    """
    Class-based view for help list template
    """
    template_name = 'help/list.html'
    model = models.HelpItem

    def get_queryset(self):
        return help_queryset(self)
