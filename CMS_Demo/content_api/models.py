from django.db import models

# Create your models here.
class ContentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class FieldDefinition(models.Model):
    name = models.CharField(max_length=100)
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
    
class ContentItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='items')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.content_type.name} - {self.slug}"

class FieldValue(models.Model):
    VALUE_TYPES = [
        ('text', 'Text'),
        ('binary', 'Binary'),
    ] 

    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='field_values')
    field_definition = models.ForeignKey(FieldDefinition, on_delete=models.CASCADE)

    value_type = models.CharField(max_length=20, choices=VALUE_TYPES)
    text_value = models.TextField(blank=True, null=True)
    binary_value = models.BinaryField(blank=True, null=True)


    def __str__(self):
        return f"{self.content_item.slug} - {self.field_definition.name}"
    
    def get_value(self):
        if self.value_type == 'text':
            return self.text_value
        elif self.value_type == 'binary':
            return self.binary_value
        return None

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.value_type == 'text' and not self.text_value:
            raise ValidationError("Text value must be provided for value_type 'text'.")
        if self.value_type == 'binary' and not self.binary_value:
            raise ValidationError("Binary value must be provided for value_type 'binary'.")


