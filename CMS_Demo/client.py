from django.utils.text import slugify
import requests
import base64

endpoint = "http://127.0.0.1:8000/content_api/content_items/"
# content_type = input("Enter the content_type(book|video|blog_post): ")
# slug = slugify(input("Enter the name for the content-item: "))
# published = False
# version = 1


response = requests.get(endpoint)

print(response.status_code)
print(response.text)


# endpoint = "http://127.0.0.1:8000/content_api/field_values/10/field/title/"
# value_type = input("Enter the value type(text|binary): ")

# value = "This is the changed text!"

# response = requests.delete(endpoint)

# print(response.status_code)
# print(response.text)