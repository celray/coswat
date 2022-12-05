#!/bin/python3
'''
this module handles logic for extracting shapefiles for
a selected outlet point for the CoSWAT Plus model

author  : Celray James CHAWANDA
email   : celray.chawanda@outlook.com
date    : 21/11/2022
repo    : https://github.com/celray

licence : All rights reserved
(c)     : Celray James CHAWANDA
'''


from cjfx import geopandas, pandas, create_path, random, list_files, delete_file, wait, exists, ignore_warnings
import numpy

ignore_warnings()


# set variables
shapes_dir = "/media/cjames/windows/GitHub/tools/CoSWAT-Global-Model/model-setup/CoSWATv0.2.2/africa-chad/Watershed/Shapes"

point_fn = f'/media/cjames/windows/GitHub/tools/CoSWAT-Global-Model/model-setup/CoSWATv0.2.2/africa-chad/Evaluation/Shape/indices.gpkg'
lsus_fn = f'{shapes_dir}/lsus2.shp'
rivers_fn = f'{shapes_dir}/rivs1.shp'

out_dir_shp = create_path("/media/cjames/windows/GitHub/websites/coswat/assets/model-data/africa/major-basins/major-basins/chad/")
network_dir = out_dir_shp
lsus_dir = out_dir_shp
points_dir = create_path("./tmp_delete/shapefiles/points/")

# read shapes
point_gpd = geopandas.read_file(point_fn).to_crs('EPSG:4326')
lsus_gpd = geopandas.read_file(lsus_fn).to_crs('EPSG:4326')
rivers_gpd = geopandas.read_file(rivers_fn).to_crs('EPSG:4326')

new_network = rivers_gpd[0:0]

current_min = {}
selected_rivers = {}

for index, row in point_gpd.iterrows():
    # this block turned out to be unnecessary as model evaluation
    # already picks the channels selected, still left here because
    # it might be useful in the future
    for index_riv, row_riv in rivers_gpd.iterrows():
        distance = (row_riv['geometry'].distance(row['geometry']))
        if not row.channel in selected_rivers:
            current_min[row.channel] = distance
            selected_rivers[row.channel] = row_riv['Channel']
        elif distance < current_min[row.channel]:
            current_min[row.channel] = distance
            selected_rivers[row.channel] = row_riv['Channel']


for selected_river in selected_rivers:
    print(selected_rivers[selected_river])
    all_points = []

    for index_riv, row_riv in rivers_gpd.iterrows():
        if not row_riv['Channel'] == selected_rivers[selected_river]: continue # print(row_riv['geometry'][0])

        x,y = row_riv['geometry'].coords.xy # print(x[-1]) # print(y[-1])
        point=geopandas.GeoDataFrame(geometry=geopandas.points_from_xy([x[-1]],[y[-1]]), crs=rivers_gpd.crs)
        
        create_path(f'{out_dir_shp}/.points/')
        point.to_file(f'{out_dir_shp}/.points/{selected_rivers[selected_river]}_inlet.geojson', driver = "GeoJSON")

        all_points.append(point)
        # done_rivers.append(selected_rivers[selected_river])
        # print(done_rivers)
        break


    done_rivers = []
    repeat = True
    while repeat:
        repeat = False

        for index_riv, row_riv in rivers_gpd.iterrows():

            current_river = row_riv['Channel']
            # if current_river in done_rivers: continue

            for point in all_points:
                if (row_riv['geometry'].touches(point['geometry'][0])):
                    if not current_river in done_rivers:
                        done_rivers.append(current_river)
                        x,y = row_riv['geometry'].coords.xy

                        pt = geopandas.GeoDataFrame(geometry=geopandas.points_from_xy([x[-1]],[y[-1]]), crs=rivers_gpd.crs)
                        pt.to_file(f'{out_dir_shp}/.points/{current_river}_inlet.geojson', driver = "GeoJSON")
                        all_points.append(pt)
                        repeat = True
                        break
            
            if repeat:
                break

    data = {
        "geometry"  : [],
        "channel"   : [],
    }

    safe_name = None
    for index_riv, row_riv in rivers_gpd.iterrows():
        if row_riv['Channel'] in done_rivers:
            data['geometry'].append(row_riv['geometry'])
            data['channel'].append(row_riv['Channel'])
            safe_name = selected_rivers[selected_river]
        if safe_name is None:
            safe_name = f"{random.randint(1,100)}"

    new_network = geopandas.GeoDataFrame(pandas.DataFrame.from_dict(data), geometry='geometry', crs=rivers_gpd.crs)
    create_path(f'{out_dir_shp}/.network/')
    new_network.to_file(f'{out_dir_shp}/.network/{safe_name}.geojson', driver = "GeoJSON")


    data = {
        "geometry"  : [],
        "channel"   : [],
    }
    for index, row_lsus in lsus_gpd.iterrows():
        if row_lsus['Channel'] in done_rivers:
                data['geometry'].append(row_lsus['geometry'])
                data['channel'].append(row_lsus['Channel'])

    new_lsus = geopandas.GeoDataFrame(pandas.DataFrame.from_dict(data), geometry='geometry', crs=rivers_gpd.crs)
    
    create_path(f'{out_dir_shp}/{safe_name}/')
    new_lsus.to_file(f'{out_dir_shp}/{safe_name}/lsus.geojson', driver = "GeoJSON")
    new_lsus = new_lsus.dissolve()
    new_lsus.to_file(f'{out_dir_shp}/{safe_name}.geojson', driver = "GeoJSON")



# find differences and clip them
intersection = True
while intersection:
    # print("master-loop")
    intersection = False
    done_lsus = []
    lsus_all = list_files(f"{lsus_dir}/", 'gpkg')
    for p_lsu_fn in lsus_all:
        if p_lsu_fn in done_lsus: continue
        # print("--main-loop--")
        for s_lsu_fn in lsus_all:
            if p_lsu_fn == s_lsu_fn: continue
            if s_lsu_fn in done_lsus: continue

            primary_lsu = geopandas.read_file(p_lsu_fn)
            secondary_lsu = geopandas.read_file(s_lsu_fn)

            # print("--second-loop--")

            if len(primary_lsu.clip(secondary_lsu).index) == 0: continue
            if (primary_lsu.clip(secondary_lsu).iloc[0]['geometry'].area > 0) or (secondary_lsu.clip(primary_lsu).iloc[0]['geometry'].area > 0):
                print(f"\nintersection between \n\t> {p_lsu_fn} and \n\t> {s_lsu_fn}")
                done_lsus.append(p_lsu_fn); done_lsus.append(s_lsu_fn)
                if primary_lsu.iloc[0]['geometry'].area > secondary_lsu.iloc[0]['geometry'].area:
                    new_lsu = primary_lsu.difference(secondary_lsu)
                    delete_file(p_lsu_fn)
                    new_lsu.to_file(p_lsu_fn, driver = "GPKG")
                    
                    intersection = True
                    print(f"replacing: {p_lsu_fn}")
                    break
                else:
                    new_lsu = secondary_lsu.difference(primary_lsu)
                    delete_file(s_lsu_fn)
                    new_lsu.to_file(s_lsu_fn, driver = "GPKG")
                    intersection = True
                    print(f"replacing: {s_lsu_fn}")
                    break
        if intersection:
            break   


