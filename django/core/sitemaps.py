from django.contrib.sitemaps import Sitemap
from help import models as helpmodels
from palaeography import models as palaeographymodels
from django.urls import reverse


class StaticPagesSitemap(Sitemap):
    """
    Sitemap: Static pages that have no data models (e.g. welcome, some about pages, etc.)
    """

    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return ['general:welcome',
                'general:about',
                'general:cookies',
                'general:accessibility']

    def location(self, obj):
        return reverse(obj)


class HelpItemListSitemap(Sitemap):
    """
    Sitemap: HelpItem List
    """

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['help:list']

    def location(self, obj):
        return reverse(obj)


class HelpItemDetailSitemap(Sitemap):
    """
    Sitemap: HelpItem Detail
    """

    priority = 0.5

    def items(self):
        return helpmodels.HelpItem.objects.filter(admin_published=True)


class DocumentListSitemap(Sitemap):
    """
    Sitemap: Document List
    """

    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ['palaeography:document-list']

    def lastmod(self, obj):
        try:
            return palaeographymodels.Document.objects.filter(admin_published=True).order_by('-meta_created_datetime')[0].meta_created_datetime
        except IndexError:
            return None

    def location(self, obj):
        return reverse(obj)


class DocumentDetailSitemap(Sitemap):
    """
    Sitemap: Document Detail
    """

    priority = 1.0

    def items(self):
        return palaeographymodels.Document.objects.filter(admin_published=True)
