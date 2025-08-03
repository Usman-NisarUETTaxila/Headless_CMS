from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedOrAdminUser
from .models import ContentItem, FieldValue, ContentType, FieldDefinition
from .serializer import ContentItemSerializer, FieldValueSerializer, ContentTypeSerializer, FieldDefinitionSerializer
import base64

# Create your views here.
class ContentItemListCreateUpdateDestroy(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
    ):
    queryset = ContentItem.objects.all()
    print(queryset)
    serializer_class = ContentItemSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrAdminUser]


    def get(self, request, *args, **kwargs):
        if kwargs != {}:
            try:
                content_item = ContentItem.objects.get(pk=kwargs.get('pk'))
                content_item_attributes = list(FieldValue.objects.filter(content_item=content_item))
                print("Attributes",content_item_attributes)
                serializer = ContentItemSerializer(content_item)
                serializer2 = FieldValueSerializer(content_item_attributes, many=True)

                # Preprocessing 
                data = serializer.data
                data["content_type"] = content_item.content_type.name
                temp = serializer2.data
                for i,attr in enumerate(content_item_attributes):
                    temp[i]["content_item"] = attr.content_item.slug
                    temp[i]["field_definition"] = attr.field_definition.name
                data["Attributes"] = temp

                return Response(data=data, status=status.HTTP_200_OK)
            except ContentItem.DoesNotExist:
                return Response({"detail": "Item Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = list(ContentItem.objects.all())
            api_data = []
            for item in items:
                content_item = item
                content_item_attributes = list(FieldValue.objects.filter(content_item=content_item))
                print("Attributes",content_item_attributes)
                serializer = ContentItemSerializer(content_item)
                serializer2 = FieldValueSerializer(content_item_attributes, many=True)

                # Preprocessing 
                data = serializer.data
                data["content_type"] = content_item.content_type.name
                temp = serializer2.data
                for i,attr in enumerate(content_item_attributes):
                    temp[i]["content_item"] = attr.content_item.slug
                    temp[i]["field_definition"] = attr.field_definition.name
                data["Attributes"] = temp
                
                api_data.append(data)
            return Response(data=api_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        post_data = request.data
        content_type_obj = ContentType.objects.filter(name=post_data['content_type']).first()
        if not content_type_obj:
            return Response({"error": "ContentType not found."}, status=status.HTTP_400_BAD_REQUEST)

        content_type = content_type_obj.pk
        slug = post_data['slug']
        published = post_data['published']
        version = post_data['version']
        data_to_save = {
            "content_type": content_type,
            "slug": slug,
            "published": published,
            "version": version 
        } 
        serializer = ContentItemSerializer(data=data_to_save)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "ContentItem Created Successfully!"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        try:
            update_data = request.data
            content_item = ContentItem.objects.get(pk=kwargs.get('pk'))

            content_type_obj = ContentType.objects.filter(name=update_data['content_type']).first()
            if not content_type_obj:
                return Response({"error": "ContentType not found."}, status=status.HTTP_400_BAD_REQUEST)

            content_type = content_type_obj.pk
            update_data["content_type"] = content_type
            serializer = ContentItemSerializer(content_item, data=update_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "ContentItem Updated Successfully!"}, status=status.HTTP_202_ACCEPTED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except ContentItem.DoesNotExist:
            return Response({"detail": "ContentItem Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            content_item = ContentItem.objects.get(pk=kwargs.get('pk'))
            content_item_attributes = list(FieldValue.objects.filter(content_item=content_item))
            if content_item_attributes != []:
                for attr in content_item_attributes:
                    attr.delete()
            content_item.delete()
            return Response({"Message": "ContentItem Deleted Successfully!"}, status=status.HTTP_200_OK)
        except ContentItem.DoesNotExist:
            return Response({"detail": "Item Not Found!"}, status=status.HTTP_404_NOT_FOUND)

class FieldValueListCreateUpdateDestroy(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
    ):
    queryset = FieldValue.objects.all()
    print(queryset)
    serializer_class = FieldValueSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            post_data = request.data
            content_item_obj = ContentItem.objects.get(pk=kwargs.get('pk'))
            field_definition_obj = FieldDefinition.objects.filter(name=post_data['field_def']).first()
            
            if post_data['value_type'] == 'text':
                field_value_instance = FieldValue(content_item=content_item_obj, field_definition=field_definition_obj, value_type="text", text_value=post_data["value"])
            elif post_data['value_type'] == 'binary':
                binary_data = base64.b64decode(post_data["value"])
                field_value_instance = FieldValue(content_item=content_item_obj, field_definition=field_definition_obj, value_type="binary", binary_value=binary_data)
            else:
                return Response({"error": "Invalid Value Type!"},status=status.HTTP_400_BAD_REQUEST)

            if field_value_instance:
                field_value_instance.save()
                return Response({"Message": "Field Value Created Successfully!"},status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Invalid Data!"},status=status.HTTP_400_BAD_REQUEST)
        except ContentItem.DoesNotExist:
            return Response({"detail": "ContentItem Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        except FieldDefinition.DoesNotExist:
            return Response({"detail": "Field Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, *args, **kwargs):
        try:
            update_data = request.data
            content_item = ContentItem.objects.get(pk=kwargs.get('pk'))
            field_name = kwargs.get('name')
            field_def = FieldDefinition.objects.filter(name=field_name).first()
            if not field_def:
                return Response({"error": "FieldDefinition not found"}, status=400)

            field_value = FieldValue.objects.filter(content_item=content_item, field_definition=field_def).first()
            if not field_value:
                return Response({"detail": "FieldValue not found"}, status=status.HTTP_404_NOT_FOUND)
                
            missing_message = []
            def update_model_from_dict(instance, data: dict):
                model_fields = [f.name for f in instance._meta.get_fields() if f.editable and not f.auto_created]

                for key in data:
                    if key in model_fields:
                        setattr(instance, key, data[key])
                    else:
                        missing_message.append(f" |{key} not matched| ")

                return instance
                          
            updated_field_value = update_model_from_dict(field_value, update_data)
            updated_field_value.save()
            return Response({"Message": "Field Value Updated Successfully!",
                             "Not Matched": missing_message}, status=status.HTTP_202_ACCEPTED)                
        
        except ContentItem.DoesNotExist:
            return Response({"detail": "Item Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            content_item = ContentItem.objects.get(pk=kwargs.get('pk'))
            field_name = kwargs.get('name')
            field_def = FieldDefinition.objects.filter(name=field_name).first()
            if not field_def:
                return Response({"error": "FieldDefinition not found"}, status=400)

            field_value = FieldValue.objects.filter(content_item=content_item, field_definition=field_def).first()
            if not field_value:
                return Response({"detail": "FieldValue not found"}, status=status.HTTP_404_NOT_FOUND)
            
            field_value.delete()
            return Response({"Message": "Field Value Deleted Successfully!"}, status=status.HTTP_200_OK)
        except ContentItem.DoesNotExist:
            return Response({"detail": "Item Not Found!"}, status=status.HTTP_404_NOT_FOUND)
            
class ContentTypeList(generics.ListAPIView):
    queryset = ContentType.objects.all()
    print(queryset)
    serializer_class = ContentTypeSerializer

class FieldDefinitionList(generics.ListAPIView):
    queryset = FieldDefinition.objects.all()
    print(queryset)
    serializer_class = FieldDefinitionSerializer