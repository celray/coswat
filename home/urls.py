
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [

    # assets paths
    re_path(r'css/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_css, name = 'get_css'),
    re_path(r'js/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_js, name = 'get_js'),
    re_path(r'images/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_images, name = 'images_view'),
    re_path(r'shapefiles/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_shapefile, name = 'get_shapefile'),

    re_path(r'continents/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)/basin-streams/(?P<basin_id>[A-Za-z0-9&\&\%\s\-._\']+)-streams.geojson', views.get_subbasin_streams, name = 'get_subbasin_streams'),
    re_path(r'continents/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)/major-basins/major-basins.geojson', views.get_major_subbasins_file, name = 'get_major_subbasins_file'),
    re_path(r'continents/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_continent_file, name = 'get_continent_file'),
    re_path(r'continents/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_continents, name = 'get_continents'),

    # page paths
    path('', views.home, name='home'),
    re_path(r'zoom-region/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)', views.view_continent, name = 'get_continents'),

    



]
