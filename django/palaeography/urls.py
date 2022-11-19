from django.urls import path
from .views import document

app_name = 'palaeography'

urlpatterns = [
    # Document
    path('documents/', document.DocumentListView.as_view(), name='document-list'),
    path('documents/<pk>/', document.DocumentDetailView.as_view(), name='document-detail'),

    # Document Image Part
    path('documents/imagepart/add', document.DocumentImagePartAddRedirectView.as_view(), name='document-imagepart-add'),
    path('documents/imagepart/delete', document.DocumentImagePartDeleteRedirectView.as_view(), name='document-imagepart-delete'),
]
