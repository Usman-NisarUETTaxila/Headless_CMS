from django.utils.text import slugify
import requests
import base64
from getpass import getpass

# username = input("Username ")
# password = getpass()

# endpoint2 = "http://localhost:8000/content_api/auth/"


# get_response2 = requests.post(endpoint2, json={"username":username,
#                                              "password": password})


# print(get_response2.json())

# if get_response2.status_code == 200:
    # token = get_response2.json()['token']
headers = {
    "Authorization": "Token 72852a7a888d7d7891503b241d3f46803b63acfb"
}
data = {
    "value_type": "text",
    "text_value": "This is the changed token blog title"
}
endpoint1 = "http://localhost:8000/content_api/content_items/15/"
get_response1 = requests.delete(endpoint1, headers=headers)
print(get_response1.status_code)


# endpoint = "http://127.0.0.1:8000/content_api/field_values/10/field/title/"
# value_type = input("Enter the value type(text|binary): ")

# value = "This is the changed text!"

# response = requests.delete(endpoint)

# print(response.status_code)
# print(response.text)