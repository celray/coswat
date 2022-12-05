
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [

    # assets paths
    re_path(r'css/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_css, name = 'get_css'),
    re_path(r'js/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_js, name = 'get_js'),
    re_path(r'images/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_images, name = 'images_view'),
    re_path(r'shapefiles/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_shapefile, name = 'get_shapefile'),

    re_path(r'layer_loader_frame/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)/(?P<major_id>[A-Za-z0-9&\&\%\s\-._\']+)', views.load_gaged_shapes, name = 'load_gaged_shapes'),

    re_path(r'continents/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)/gaged-lsus/(?P<major_id>[A-Za-z0-9&\&\%\s\-._\']+)/(?P<lsu_id>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_gaged_lsu, name = 'get_gaged_lsu'),
    re_path(r'continents/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)/basin-streams/(?P<basin_file>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_subbasin_file, name = 'get_subbasin_file'),
    re_path(r'continents/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)/major-basins/major-basins.geojson', views.get_major_subbasins_file, name = 'get_major_subbasins_file'),
    re_path(r'continents/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_continent_file, name = 'get_continent_file'),
    re_path(r'continents/(?P<file_name>[A-Za-z0-9&\&\%\s\-._\']+)', views.get_continents, name = 'get_continents'),

    # page paths
    # path('', views.home, name='home'),
    path('', views.home_map, name='home_map'),
    # re_path(r'zoom-region/(?P<continent>[A-Za-z0-9&\&\%\s\-._\']+)', views.home_map, name = 'home_map'),

    



]
