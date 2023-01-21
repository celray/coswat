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

    welcome = models.welcome.objects.all()
    welcome = welcome[0] if len(welcome) > 0 else None

    args = {
        "page_title"    : "CoSWAT Plus - The Community SWAT+ Model",
        'welcome'       : welcome,
        'csrf_token'    : get_token(request),
    }

    response = render(request=request, template_name='home.html', context=args)
    return response



def home_map(request):


    welcome = models.welcome.objects.all()
    welcome = welcome[0] if len(welcome) > 0 else None

    args = {
        "page_title"        : f"CoSWAT Plus - The Community SWAT+ Model",
        'welcome'           : welcome,
        "index"             : 1,
        "details_pannel"    : True,

        'csrf_token'        : get_token(request)

    }

    response = render(request=request, template_name='showcase.html', context=args)
    return response





def datasets(request):

    datasets_sources  = models.model_data.objects.all()





    args = {
        "page_title"            : f"Datasets - CoSWAT Plus",
        "index"                 : 2,
        "datasets_sources"      : datasets_sources,

        'csrf_token'    : get_token(request)

    }

    response = render(request=request, template_name='main-datasets.html', context=args)
    return response


def scripts(request):

    args = {
        "page_title"            : f"Scripts - CoSWAT Plus",
        "index"                 : 3,

        'csrf_token'    : get_token(request)

    }

    response = render(request=request, template_name='main-scripts.html', context=args)
    return response


def outputs(request):

    args = {
        "page_title"            : f"Outputs - CoSWAT Plus",
        "index"                 : 4,

        'csrf_token'    : get_token(request)

    }

    response = render(request=request, template_name='main-outputs.html', context=args)
    return response




def calibration(request):

    args = {
        "page_title"            : f"Calibration - CoSWAT Plus",
        "index"                 : 5,

        'csrf_token'    : get_token(request)

    }

    response = render(request=request, template_name='main-calibration.html', context=args)
    return response




def about(request):

    about = models.about.objects.all()[0] if len(models.about.objects.all()) > 0 else None

    args = {
        "page_title"            : f"About - CoSWAT Plus",
        "index"                 : 6,

        "about"                 : about,
        'csrf_token'    : get_token(request)

    }

    response = render(request=request, template_name='main-about.html', context=args)

    
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"


    return response






def edit_profile(request):

    myProfile = models.profile.objects.all().get(user = request.user)
    if request.method == "GET":

        args = {
            "page_title"            : f"Edit Profile - CoSWAT-GM",
            "index"                 : -1,

            "myProfile"             : myProfile,
            'csrf_token'    : get_token(request)

        }

    if request.method == "POST":

        first_name  = request.POST['first_name']
        last_name   = request.POST['last_name']

        # username    = request.POST['username']
        email       = request.POST['email']

        bio         = request.POST['bio']           # can be ""
        country     = request.POST['country']       # can be ""
        city        = request.POST['city']          # can be ""
        link        = request.POST['link']          # can be ""

        new_ppicture = False
        if 'file_name_' in request.FILES:
            new_ppicture = request.FILES['file_name_']

        myProfile.user.email = email
        myProfile.user.username = email
        myProfile.user.first_name = first_name
        myProfile.user.last_name = last_name

        if not bio == "":
            myProfile.bio = bio

        if not link == "":
            myProfile.personal_link = link

        if (not country == "") and (not city == ""):
            myProfile.location = f"{country}, {city}"
        elif not country == "":
            myProfile.location = country

        if not new_ppicture == False:
            myProfile.image = new_ppicture
        
        myProfile.user.save()
        myProfile.save()

        return redirect("/my-profile")



    response = render(request=request, template_name='profile-edit.html', context=args)
    
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    return response





def my_profile(request):

    myProfile = models.profile.objects.all().get(user = request.user)

    args = {
        "page_title"            : f"My Profile - CoSWAT-GM",
        "index"                 : -1,

        "myProfile"             : myProfile,
        'csrf_token'    : get_token(request)

    }

    response = render(request=request, template_name='profile-details.html', context=args)

    
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

    asset_classes = ["images", "profile-pictures", "ppictures", "pictures", "photos"]

    for asset_class in asset_classes:
        download_path = os.path.join(settings.BASE_DIR, f"assets/{asset_class}", file_name)
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


def get_hydrograph(request, zone, channel, station_id):

    continent   = zone.split('-')[0]
    basin       = zone.split('-')[1]

    download_path = os.path.join(settings.BASE_DIR, f"assets/model-setups/{continent}/{basin}/figures/", f"{channel}-{station_id}.png")
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
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404


def get_gaged_lsu(request, continent, major_id, lsu_id):
    download_path = os.path.join(settings.BASE_DIR, f"assets/model-data/{continent}/major-basins/major-basins/{major_id}/{lsu_id}.geojson")
    
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404



def get_subregion_shape(request, continent, subbasin, subregion_id):
    # model-data\africa\major-basins\major-basins\save
    download_path = os.path.join(settings.BASE_DIR, f"assets/model-data/{continent}/major-basins/major-basins/{subbasin}/{subregion_id}.geojson")
    print(download_path)
    
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(download_path)
            return response
    raise Http404




def get_favicon(request):
    # model-data\africa\major-basins\major-basins\save
    download_path = os.path.join(settings.BASE_DIR, f"assets/images/favion.ico")
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
        'csrf_token'    : get_token(request)

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

        # print(current_url)
        # print(username)
        # print(password)

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
    args = { 
        # 'csrf_token'    : get_token(request)
    }

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


