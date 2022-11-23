from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
# from . import models, forms
from django.utils.timezone import make_aware

from django.conf import settings
from django.contrib.auth.hashers import make_password

import os




def home(request):

    args = {
        "page_title"            : "CoSWAT Plus - The Community SWAT+ Model",
    }

    response = render(request=request, template_name='home.html', context=args)
    return response





def view_continent(request, continent):

    args = {
        "page_title"            : f"CoSWAT Plus - {continent}",
        "continent"             : continent,
    }

    response = render(request=request, template_name='continent.html', context=args)
    return response

























def get_css(request, file_name=''):
    
    file_name = os.path.basename(file_name)
    download_path = os.path.join(settings.BASE_DIR, "assets/css", file_name)
    
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="text/css")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404

def get_js(request, file_name=''):
    
    file_name = os.path.basename(file_name)
    download_path = os.path.join(settings.BASE_DIR, "assets/js", file_name)
    
    print(download_path)
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="text/javascript")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404


def get_images(request, file_name=''):
    
    file_name = os.path.basename(file_name)

    asset_classes = ["attachments", "global", "icons", "pictures", "profile-pictures"]

    for asset_class in asset_classes:
        download_path = os.path.join(settings.BASE_DIR, "assets/images", file_name)
        if os.path.exists(download_path):
            break

    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404



def get_shapefile(request, file_name=''):
    
    file_name = os.path.basename(file_name)

    download_path = os.path.join(settings.BASE_DIR, "assets/shapefiles", file_name)

    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404



def get_continents(request, file_name):
    file_name = os.path.basename(file_name)

    download_path = os.path.join(settings.BASE_DIR, "assets/model-data/global", file_name)
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404


def get_continent_file(request, continent, file_name):
    
    file_name = os.path.basename(file_name)

    download_path = os.path.join(settings.BASE_DIR, f"assets/model-data/{continent}", file_name)
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404


def get_major_subbasins_file(request, continent):
    

    download_path = os.path.join(settings.BASE_DIR, f"assets/model-data/{continent}/major-basins/major-basins.geojson")
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404



def get_subbasin_streams(request, continent, basin_id):
    
    download_path = os.path.join(settings.BASE_DIR, f"assets/model-data/{continent}/major-basins/major-basins/{basin_id}-streams.geojson")
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404


