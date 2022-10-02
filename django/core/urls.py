from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from . import sitemaps

# sitemaps = {
#     'static-pages': sitemaps.StaticPagesSitemap,

#     'help:list': sitemaps.HelpItemListSitemap,
#     'help:detail': sitemaps.HelpItemDetailSitemap,

#     'palaeography:document-list': sitemaps.ItemListSitemap,
#     'palaeography:document-detail': sitemaps.ItemDetailSitemap,
# }


urlpatterns = i18n_patterns(

    # Custom apps
    path('', include('general.urls')),
    path('help/', include('help.urls')),
    path('palaeography/', include('palaeography.urls')),

    # Account app's urls + Django's built in auth's urls
    # Share same pattern (/account) for consistency for user
    # Account app's urls must appear above Django's auth's urls to take priority
    path('account/', include('account.urls')),
    path('account/', include('django.contrib.auth.urls')),

    # Django admin
    path('dashboard/', admin.site.urls),

    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),

    # Sitemap
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
