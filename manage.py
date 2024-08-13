#!/usr/bin/env python
#!/usr/bin/env python
import os
import sys
import ee
import google.auth.exceptions


# Function to initialize GEE
# def initialize_gee():
#     service = os.getenv('SA')
#     file = r"D:\Desktop\Django_app_12_sep-2023\gee\ee-muzzamil.json"
#     credentials = ee.ServiceAccountCredentials(service, file)
#     ee.Initialize(credentials)
    

# Function to refresh GEE token
# def refresh_gee_token():
#     if not ee.data.getAssetRoots():
#         initialize_gee()
from google.auth.transport.requests import Request




def inv():
    service = os.getenv('SA')
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'gee','ee-muzzamil1-37ebc3dece52.json')
    print(file)
    credentials = ee.ServiceAccountCredentials(service, file)
    try:
        ee.Initialize(credentials)
    except google.auth.exceptions.RefreshError as e:
        # If the token has expired, refresh it
        request = Request()
        credentials.refresh(request)
        ee.Initialize(credentials)



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoGEE.settings")
    # initialize_gee()
    # refresh_gee_token()
    inv()
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Add a call to refresh_gee_token() before executing Django commands
    # refresh_gee_token()

    execute_from_command_line(sys.argv)
