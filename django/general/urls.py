from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'general'

urlpatterns = [
    path('', RedirectView.as_view(url='welcome', permanent=False), name='index'),
    path('welcome/', views.WelcomeTemplateView.as_view(), name='welcome'),

    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('about/accessibility/', views.AccessibilityTemplateView.as_view(), name='accessibility'),
    path('about/cookies/', views.CookiesTemplateView.as_view(), name='cookies'),

    path('robots.txt', views.RobotsTemplateView.as_view(), name='robots')
]
