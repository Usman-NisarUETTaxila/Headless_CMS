"""
URL configuration for CMS_Demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from .views import ContentItemListCreateUpdateDestroy, FieldValueListCreateUpdateDestroy, ContentTypeList, FieldDefinitionList

urlpatterns = [
    path('content_items/', ContentItemListCreateUpdateDestroy.as_view()),
    path('content_items/<int:pk>/', ContentItemListCreateUpdateDestroy.as_view()),
    path('field_values/', FieldValueListCreateUpdateDestroy.as_view()),
    path('field_values/<int:pk>/field/<str:name>/', FieldValueListCreateUpdateDestroy.as_view()),
    path('content_types/', ContentTypeList.as_view()),
    path('field_definitions/', FieldDefinitionList.as_view()),
]
