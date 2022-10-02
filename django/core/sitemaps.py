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
                'about:project',
                'about:website',
                'about:website-cookies',
                'about:website-accessibility']

    def location(self, obj):
        return reverse(obj)


class AboutNewsItemListSitemap(Sitemap):
    """
    Sitemap: About - NewsItem List
    """

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['about:newsitem-list']

    def location(self, obj):
        return reverse(obj)


class AboutNewsItemDetailSitemap(Sitemap):
    """
    Sitemap: About - NewsItem Detail
    """

    priority = 0.5

    def items(self):
        return aboutmodels.NewsItem.objects.filter(admin_published=True)


class AboutTeamMemberListSitemap(Sitemap):
    """
    Sitemap: About - TeamMember List
    """

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['about:teammember-list']

    def location(self, obj):
        return reverse(obj)


class AboutTeamMemberDetailSitemap(Sitemap):
    """
    Sitemap: About - TeamMember Detail
    """

    priority = 0.5

    def items(self):
        return aboutmodels.TeamMember.objects.filter(admin_published=True)


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


class GraphicElementListSitemap(Sitemap):
    """
    Sitemap: GraphicElement List
    """

    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['palaeography:graphicelement-list']

    def lastmod(self, obj):
        try:
            return palaeographymodels.GraphicElement.objects.order_by('-meta_created_datetime')[0].meta_created_datetime
        except IndexError:
            return None

    def location(self, obj):
        return reverse(obj)


class GraphicElementDetailSitemap(Sitemap):
    """
    Sitemap: GraphicElement Detail
    """

    priority = 0.9

    def items(self):
        return palaeographymodels.GraphicElement.objects.filter(admin_published=True)


class ItemImageListSitemap(Sitemap):
    """
    Sitemap: ItemImage List
    """

    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['palaeography:itemimage-list']

    def lastmod(self, obj):
        try:
            return palaeographymodels.ItemImage.objects.order_by('-meta_created_datetime')[0].meta_created_datetime
        except IndexError:
            return None

    def location(self, obj):
        return reverse(obj)


class ItemImageDetailSitemap(Sitemap):
    """
    Sitemap: ItemImage Detail
    """

    priority = 0.9

    def items(self):
        return palaeographymodels.ItemImage.objects.filter(admin_published=True)


class ItemListSitemap(Sitemap):
    """
    Sitemap: Item List
    """

    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['palaeography:document-list']

    def lastmod(self, obj):
        try:
            return palaeographymodels.Item.objects.order_by('-meta_created_datetime')[0].meta_created_datetime
        except IndexError:
            return None

    def location(self, obj):
        return reverse(obj)


class ItemDetailSitemap(Sitemap):
    """
    Sitemap: Item Detail
    """

    priority = 0.9

    def items(self):
        return palaeographymodels.Item.objects.filter(admin_published=True)


class HandListSitemap(Sitemap):
    """
    Sitemap: Hand List
    """

    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['palaeography:hand-list']

    def lastmod(self, obj):
        try:
            return palaeographymodels.Hand.objects.order_by('-meta_created_datetime')[0].meta_created_datetime
        except IndexError:
            return None

    def location(self, obj):
        return reverse(obj)


class HandDetailSitemap(Sitemap):
    """
    Sitemap: Hand Detail
    """

    priority = 0.9

    def items(self):
        return palaeographymodels.Hand.objects.filter(admin_published=True)


class ScribeListSitemap(Sitemap):
    """
    Sitemap: Scribe List
    """

    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['palaeography:scribe-list']

    def lastmod(self, obj):
        try:
            return palaeographymodels.Scribe.objects.order_by('-meta_created_datetime')[0].meta_created_datetime
        except IndexError:
            return None

    def location(self, obj):
        return reverse(obj)


class ScribeDetailSitemap(Sitemap):
    """
    Sitemap: Scribe Detail
    """

    priority = 0.9

    def items(self):
        return palaeographymodels.Scribe.objects.filter(admin_published=True)
