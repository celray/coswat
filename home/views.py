from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from . import models
from django.utils.timezone import make_aware

from django.conf import settings
from django.contrib.auth.hashers import make_password

import os
from glob import glob
from django.middleware.csrf import get_token













def home(request):

    args = {
        "page_title"            : "CoSWAT Plus - The Community SWAT+ Model",
        'csrf_token' : get_token(request)
    }

    response = render(request=request, template_name='home.html', context=args)
    return response



def home_map(request):

    args = {
        "page_title"            : f"CoSWAT Plus - The Community SWAT+ Model",
        "index"                 : 1,
        "details_pannel"        : True
    }

    response = render(request=request, template_name='home-map.html', context=args)
    return response





def datasets(request):

    datasets_sources  = models.model_data.objects.all()





    args = {
        "page_title"            : f"Datasets - CoSWAT Plus",
        "index"                 : 2,
        "datasets_sources"      : datasets_sources,
    }

    response = render(request=request, template_name='main-datasets.html', context=args)
    return response


def scripts(request):

    args = {
        "page_title"            : f"Scripts - CoSWAT Plus",
        "index"                 : 3
    }

    response = render(request=request, template_name='main-scripts.html', context=args)
    return response


def outputs(request):

    args = {
        "page_title"            : f"Outputs - CoSWAT Plus",
        "index"                 : 4
    }

    response = render(request=request, template_name='main-outputs.html', context=args)
    return response




def calibration(request):

    args = {
        "page_title"            : f"Calibration - CoSWAT Plus",
        "index"                 : 5
    }

    response = render(request=request, template_name='main-calibration.html', context=args)
    return response




def about(request):

    args = {
        "page_title"            : f"About - CoSWAT Plus",
        "index"                 : 6
    }

    response = render(request=request, template_name='main-about.html', context=args)

    
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"


    return response















# user management


def signin(request):

    if request.user.is_authenticated:
        return redirect("/")

    current_url = None
    if request.method == "POST":
        current_url      = f"{request.POST['current_url']}"

        print(current_url)
    args = {
            }
    return render(request, "main-signin.html", args)


def signout(request):
    logout(request)
    return redirect("/")
        

























# assets 

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


def get_subbasin_file(request, continent, basin_file):

    download_path = os.path.join(settings.BASE_DIR, f"assets/model-data/{continent}/major-basins/major-basins/{basin_file}")
    print('--')
    print(download_path)
    print('--')
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404


def get_gaged_lsu(request, continent, major_id, lsu_id):
    print('----ind------')
    download_path = os.path.join(settings.BASE_DIR, f"assets/model-data/{continent}/major-basins/major-basins/{major_id}/{lsu_id}.geojson")
    print(download_path)
    
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404











# framed responses

def load_gaged_shapes(request, continent, major_id):

    gaged_lsus_dir = os.path.join(settings.BASE_DIR, f"assets/model-data/{continent}/major-basins/major-basins/{major_id}/")
    
    file_names = list_files(gaged_lsus_dir, 'geojson')
    lsu_ids = [file_name(fn) for fn in file_names]
    
    args = {
        "lsu_ids"    : lsu_ids,
        "continent"  : continent,
        "major_id"   : major_id,
    }

    response = render(request=request, template_name='gaged_shapes_loader.html', context=args)
    return response




def signin_frame(request):

    if request.user.is_authenticated:
        return redirect("/")

    current_url = None
    if request.method == "POST":
        current_url     = f"{request.POST['current_url']}"
        username        = f"{request.POST['username']}"
        password        = f"{request.POST['password']}"

        print(current_url)
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            response = redirect('null_page')

        else:
            response = redirect('null_page')
            response.status_code = 500

        return response
    args = {
            }

    response = render(request, "frame-login.html", args)

    return response




def avatar_frame(request):
    args = { }

    response = render(request, "frame-avatar.html", args)
    return response














# generic functions

def list_files(folder, extension="*"):
    if folder.endswith("/"):
        if extension == "*":
            list_of_files = glob(folder + "*")
        else:
            list_of_files = glob(folder + "*." + extension)
    else:
        if extension == "*":
            list_of_files = glob(folder + "/*")
        else:
            list_of_files = glob(folder + "/*." + extension)
    return list_of_files


def file_name(path_, extension=False):
    if extension:
        fn = os.path.basename(path_)
    else:
        fn = os.path.basename(path_).split(".")[0]
    return(fn)


def null_page(request):
    response = render(request=request, template_name='null-page.html', context={})
    return response


