from django.urls import path
from .views.document import DocumentListView, DocumentDetailView, DocumentImagePartAddRedirectView

app_name = 'palaeography'

urlpatterns = [
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/imagepart/add', DocumentImagePartAddRedirectView.as_view(), name='document-imagepart-add'),
]
