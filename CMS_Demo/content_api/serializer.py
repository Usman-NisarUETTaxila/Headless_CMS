from rest_framework import serializers
from .models import FieldValue, FieldDefinition, ContentItem, ContentType

class FieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldValue
        fields = ["id","content_item", "field_definition", "value_type", "text_value", "binary_value"]
    
class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ["id", "name", "description"]

class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ["id", "content_type", "slug" , "created_at" , "updated_at", "published", "version"]

class FieldDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDefinition
        fields = ["id", "name"]