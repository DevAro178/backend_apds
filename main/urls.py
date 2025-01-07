"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    EmailsViewSet, ReportsViewSet, FAQsViewSet, AttachmentsViewSet, 
    CategoryViewSet, LinksViewSet, ReportAttributesViewSet, SpamClassifierView
)


# Initialize router and register viewsets
router = DefaultRouter()
router.register(r'emails', EmailsViewSet, basename='emails')
router.register(r'reports', ReportsViewSet, basename='reports')
router.register(r'faqs', FAQsViewSet, basename='faqs')
router.register(r'attachments', AttachmentsViewSet, basename='attachments')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'links', LinksViewSet, basename='links')
router.register(r'report-attributes', ReportAttributesViewSet, basename='report-attributes')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/spam-classifier/',SpamClassifierView.as_view(),name='spam-classifier'),
    path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]