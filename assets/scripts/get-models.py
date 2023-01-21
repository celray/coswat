#!/bin/python3

'''


'''



from cjfx import *
ignore_warnings()

# change working directory
me = os.path.realpath(__file__)
os.chdir(os.path.dirname(me))

args = sys.argv[1:]

if len(args) < 2:
    print(" specify 'version', 'yes or no for disolving gaged' (optional: zone)")
    quit()
elif len(args) == 2:
    version     = args[0]
    models_dir  = f"../../../../tools/CoSWAT-Global-Model/model-setup/CoSWATv{version}"
    zones       = list_folders(models_dir)
else:
    version     = args[0]
    models_dir  = f"../../../../tools/CoSWAT-Global-Model/model-setup/CoSWATv{version}"
    zones       = args[2:] 

dissolve = True if ((args[1] == 'yes') or (args[1] == 'y')) else False



all_zones = {}
final_json = None

for model_setup in zones:
    parts       = model_setup.split('-')

    continent   = parts[0]
    basin       = parts[1]

    print(f"\n\t> processing {basin}")

    create_path(f"../model-setups/{continent}/")
    
    dst_figures_dir = create_path(f"../model-setups/{continent}/{basin}/figures/")
    src_figures_dir = f"{models_dir}/{model_setup}/Evaluation/Figures/"

    figures_list = list_files(src_figures_dir)
    for fig_ in figures_list:
        copy_file(fig_, f"{dst_figures_dir}/{file_name(fig_)}", v=False)

    lsus2 = geopandas.read_file(f"{models_dir}/{model_setup}/Watershed/Shapes/lsus2.shp")
    rivs1 = geopandas.read_file(f"{models_dir}/{model_setup}/Watershed/Shapes/rivs1.shp")

    lsus2 = lsus2.to_crs('epsg:4326')
    rivs1 = rivs1.to_crs('epsg:4326')

    lsus2['name'] = f'{basin}'
    rivs1['name'] = f'{basin}'

    lsus2 = lsus2[['geometry', 'name']].dissolve()
    rivs1 = rivs1[['geometry', 'name']]

    gaged_shapes_dir = create_path(f'../model-data/{continent}/major-basins/major-basins/{basin}/')
    lsus2.to_file(f'../model-data/{continent}/major-basins/major-basins/{basin}.geojson', driver="GeoJSON")
    rivs1.to_file(f'../model-data/{continent}/major-basins/major-basins/{basin}-streams.geojson', driver="GeoJSON")

    if not f'{continent}' in all_zones:
        all_zones[f'{continent}'] = []

    all_zones[f'{continent}'].append(lsus2)

    point_json_fn   = f'{models_dir}/{model_setup}/Evaluation/Shape/indices.geojson'
    
    if exists(point_json_fn):
        point_geojson_gpd   = geopandas.read_file(point_json_fn).to_crs('EPSG:4326')
        
        if final_json is None:
            final_json = point_geojson_gpd
        else:
            final_json = geopandas.GeoDataFrame(pandas.concat([final_json, point_geojson_gpd]), geometry='geometry', crs = point_geojson_gpd.crs)


    if not dissolve:
        continue

    print ("\t  - clipping files")
    # set variables
    shapes_dir = f"{models_dir}/{model_setup}/Watershed/Shapes"

    point_fn        = f'{models_dir}/{model_setup}/Evaluation/Shape/indices.gpkg'
    lsus_fn         = f'{shapes_dir}/lsus2.shp'
    rivers_fn       = f'{shapes_dir}/rivs1.shp'

    lsus_dir = gaged_shapes_dir

    if not exists(point_fn): continue
    # read shapes
    point_gpd           = geopandas.read_file(point_fn).to_crs('EPSG:4326')
    lsus_gpd            = geopandas.read_file(lsus_fn).to_crs('EPSG:4326')
    rivers_gpd          = geopandas.read_file(rivers_fn).to_crs('EPSG:4326')

    # create tree dictionary
    
    channel_tree = {}
    for index_riv, row_riv in rivers_gpd.iterrows():
        if row_riv['ChannelR'] == 0: continue
        if not row_riv['ChannelR'] in channel_tree:
            channel_tree[row_riv['ChannelR']] = []

        if not row_riv['Channel'] in channel_tree[row_riv['ChannelR']]:
            channel_tree[row_riv['ChannelR']].append(row_riv['Channel'])


    def recurse_chanels(e_chan_, channels___):
        if not e_chan_ in channel_tree:
            return
        for channumber in channel_tree[e_chan_]:
            # if not channumber
            channels___.append(channumber)
            recurse_chanels(channumber, channels___)
            
        
        return

    
    new_network = rivers_gpd[0:0]


    current_min = {}
    selected_rivers = {}

    for index, row in point_gpd.iterrows():
        # this block turned out to be unnecessary as model evaluation
        # already picks the channels selected, still left here because
        # it might be useful in the future
        report(f'\t  - getting channel for grdc station {row.grdc_no}       ')

        for index_riv, row_riv in rivers_gpd.iterrows():
            distance = (row_riv['geometry'].distance(row['geometry']))
            if not row.channel in selected_rivers:
                current_min[row.channel] = distance
                selected_rivers[row.channel] = row_riv['Channel']
            elif distance < current_min[row.channel]:
                current_min[row.channel] = distance
                selected_rivers[row.channel] = row_riv['Channel']
    # print()

    # for selected_river in selected_rivers:
    #     print(selected_river)

    # quit()

    safe_names_kept = []
    for selected_river in selected_rivers:
        safe_names_kept.append(selected_rivers[selected_river])

    upstream_rivers = {}
    for selected_river in selected_rivers:
        # print(selected_rivers[selected_river])
        all_points = []

        report(f'\t  - assigning final points to channels: channel {selected_river}           ')

        for index_riv, row_riv in rivers_gpd.iterrows():
            if not row_riv['Channel'] == selected_rivers[selected_river]: continue # print(row_riv['geometry'][0])

            x,y = row_riv['geometry'].coords.xy # print(x[-1]) # print(y[-1])
            point=geopandas.GeoDataFrame(geometry=geopandas.points_from_xy([x[-1]],[y[-1]]), crs=rivers_gpd.crs)
            
            create_path(f'{gaged_shapes_dir}/.points/')
            point.to_file(f'{gaged_shapes_dir}/.points/{selected_rivers[selected_river]}_inlet.geojson', driver = "GeoJSON")

            all_points.append(point)
            # done_rivers.append(selected_rivers[selected_river])
            # print(done_rivers)
            break
        

        # repeat = True

        channels___ = []
        recurse_chanels(int(selected_river), channels___)
        channels___.append(selected_river)

        upstream_rivers[selected_river] = channels___


    sorted_selected_rivers = list(selected_rivers)
    
    break_loop = False
    
    while not break_loop:

        all_good = False
        for riv_idx in range(0, len(sorted_selected_rivers) - 1):
            if len(upstream_rivers[sorted_selected_rivers[riv_idx]]) < len(upstream_rivers[sorted_selected_rivers[riv_idx + 1]]):
            
                # print(len(upstream_rivers[sorted_selected_rivers[riv_idx]]), ' vs ', len(upstream_rivers[sorted_selected_rivers[riv_idx + 1]]))
                
                # print(sorted_selected_rivers)
                # print([len(upstream_rivers[riv]) for riv in sorted_selected_rivers])
                
                # print()
                keep_val = sorted_selected_rivers[riv_idx]
                del sorted_selected_rivers[riv_idx]

                sorted_selected_rivers.append(keep_val)

                # print(sorted_selected_rivers)
                # print([len(upstream_rivers[riv]) for riv in sorted_selected_rivers])
                
                all_good = False
                break
            else:
                all_good = True

            previous_lengh = len(upstream_rivers[sorted_selected_rivers[riv_idx]])
        
        break_loop = True if all_good else False


    popped = []
    for sorted_river in sorted_selected_rivers:
        
        popped.append(sorted_river)

        for sorted_river_inner in sorted_selected_rivers:

            if not sorted_river_inner in popped:

                for rnm in upstream_rivers[sorted_river_inner]:
                    if rnm in upstream_rivers[sorted_river]:
                        upstream_rivers[sorted_river].remove(rnm)

    for key in upstream_rivers:

        data = {
                "geometry"  : [],
                "channel"   : [],
            }
        for index_riv, row_riv in rivers_gpd.iterrows():
            if row_riv['Channel'] in upstream_rivers[key]:
                data['geometry'].append(row_riv['geometry'])
                data['channel'].append(row_riv['Channel'])

        new_network = geopandas.GeoDataFrame(pandas.DataFrame.from_dict(data), geometry='geometry', crs=rivers_gpd.crs)
        create_path(f'{gaged_shapes_dir}/.network/')
        new_network.to_file(f'{gaged_shapes_dir}/.network/{key}.geojson', driver = "GeoJSON")

        data = {
            "geometry"  : [],
            "channel"   : [],
        }
        for index, row_lsus in lsus_gpd.iterrows():
            if row_lsus['Channel'] in upstream_rivers[key]:
                    data['geometry'].append(row_lsus['geometry'])
                    data['channel'].append(row_lsus['Channel'])

        new_lsus = geopandas.GeoDataFrame(pandas.DataFrame.from_dict(data), geometry='geometry', crs=rivers_gpd.crs)
        
        create_path(f'{gaged_shapes_dir}/{key}/')
        new_lsus.to_file(f'{gaged_shapes_dir}/{key}/lsus.geojson', driver = "GeoJSON")

        new_lsus = new_lsus.dissolve()
        new_lsus['subregionID'] = None
        new_lsus.loc[0, 'subregionID'] = key

        report(f'\t  - saving subregion {key}                               ')
        new_lsus.to_file(f'{gaged_shapes_dir}/{key}.geojson', driver = "GeoJSON")

print()
final_major_basins = None
for continent in all_zones:
    print(f"\t# preparing major basins for {continent}")
    final_major_basins = geopandas.GeoDataFrame(pandas.concat(all_zones[continent], ignore_index=True))
    
    if not final_major_basins is None:
        final_major_basins.to_file(f'../model-data/{continent}/major-basins/major-basins.geojson', driver = 'GeoJSON')


# save all performance data

if not final_json is None:
    print(f"\t# preparing global performance for flow shapefile")
    final_json.to_file(f'../model-data/global/stations.geojson', driver = 'GeoJSON')
