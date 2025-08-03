from django.contrib import admin
from .models import ContentType, FieldDefinition, ContentItem, FieldValue

# Register your models here.
admin.site.register(ContentType)
admin.site.register(ContentItem)
admin.site.register(FieldDefinition)
admin.site.register(FieldValue)