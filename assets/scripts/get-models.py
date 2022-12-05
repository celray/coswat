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

dissolve = True if args[1] == 'yes' else False



all_zones = {}
for model_setup in zones:
    parts       = model_setup.split('-')

    continent   = parts[0]
    basin       = parts[1]

    print(f"\n\t> processing {basin}")

    create_path(f"../model-setups/{continent}/")
    create_path(f"../model-setups/{continent}/{basin}/")

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

    if not dissolve:
        continue

    print ("\t  - clipping files")
    # set variables
    shapes_dir = f"{models_dir}/{model_setup}/Watershed/Shapes"

    point_fn = f'{models_dir}/{model_setup}/Evaluation/Shape/indices.gpkg'
    lsus_fn = f'{shapes_dir}/lsus2.shp'
    rivers_fn = f'{shapes_dir}/rivs1.shp'

    lsus_dir = gaged_shapes_dir

    if not exists(point_fn): continue
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
        report(f'\t  - getting channel for grdc station {row.grdc_no}       ')

        for index_riv, row_riv in rivers_gpd.iterrows():
            distance = (row_riv['geometry'].distance(row['geometry']))
            if not row.channel in selected_rivers:
                current_min[row.channel] = distance
                selected_rivers[row.channel] = row_riv['Channel']
            elif distance < current_min[row.channel]:
                current_min[row.channel] = distance
                selected_rivers[row.channel] = row_riv['Channel']
    print()
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
                            pt.to_file(f'{gaged_shapes_dir}/.points/{current_river}_inlet.geojson', driver = "GeoJSON")
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
        create_path(f'{gaged_shapes_dir}/.network/')
        new_network.to_file(f'{gaged_shapes_dir}/.network/{safe_name}.geojson', driver = "GeoJSON")


        data = {
            "geometry"  : [],
            "channel"   : [],
        }
        for index, row_lsus in lsus_gpd.iterrows():
            if row_lsus['Channel'] in done_rivers:
                    data['geometry'].append(row_lsus['geometry'])
                    data['channel'].append(row_lsus['Channel'])

        new_lsus = geopandas.GeoDataFrame(pandas.DataFrame.from_dict(data), geometry='geometry', crs=rivers_gpd.crs)
        
        create_path(f'{gaged_shapes_dir}/{safe_name}/')
        new_lsus.to_file(f'{gaged_shapes_dir}/{safe_name}/lsus.geojson', driver = "GeoJSON")
        new_lsus = new_lsus.dissolve()
        new_lsus.to_file(f'{gaged_shapes_dir}/{safe_name}.geojson', driver = "GeoJSON")



    # find differences and clip them
    intersection = True

    past_lsus = []
    while intersection:
        # print("master-loop")
        intersection = False
        done_lsus = []
        lsus_all = list_files(f"{lsus_dir}/", 'geojson')
        for p_lsu_fn in lsus_all:
            if p_lsu_fn in done_lsus: continue
            # print("--main-loop--")
            if p_lsu_fn in past_lsus:
                continue
            report(f'\t  - removing overlaps - file: {file_name(p_lsu_fn)}                ', printing = False)
            for s_lsu_fn in lsus_all:
                if p_lsu_fn == s_lsu_fn: continue
                if s_lsu_fn in done_lsus: continue

                primary_lsu = geopandas.read_file(p_lsu_fn)
                secondary_lsu = geopandas.read_file(s_lsu_fn)

                # print("--second-loop--")

                if len(primary_lsu.clip(secondary_lsu).index) == 0: continue
                if (primary_lsu.clip(secondary_lsu).iloc[0]['geometry'].area > 0) or (secondary_lsu.clip(primary_lsu).iloc[0]['geometry'].area > 0):
                    # print(f"\n\t! intersection between \n\t> {p_lsu_fn} and \n\t> {s_lsu_fn}")
                    done_lsus.append(p_lsu_fn); done_lsus.append(s_lsu_fn)
                    if primary_lsu.iloc[0]['geometry'].area > secondary_lsu.iloc[0]['geometry'].area:
                        # report(f"\treplacing: {file_name(p_lsu_fn)}      ")
                        new_lsu = primary_lsu.difference(secondary_lsu)
                        delete_file(p_lsu_fn)
                        new_lsu.to_file(p_lsu_fn, gdriver = "geoJSON")
                        
                        intersection = True
                        break
                    else:
                        # report(f"\treplacing: {file_name(s_lsu_fn)}      ")
                        new_lsu = secondary_lsu.difference(primary_lsu)
                        delete_file(s_lsu_fn)
                        new_lsu.to_file(s_lsu_fn, gdriver = "geoJSON")
                        intersection = True
                        break
            if intersection:
                break   
            elif not p_lsu_fn in past_lsus:
                past_lsus.append(p_lsu_fn)



print()
final_major_basins = None
for continent in all_zones:
    print(f"\t# preparing major basins for {continent}")
    final_major_basins = geopandas.GeoDataFrame(pandas.concat(all_zones[continent], ignore_index=True))
    
    if not final_major_basins is None:
        final_major_basins.to_file(f'../model-data/{continent}/major-basins/major-basins.geojson', driver = 'GeoJSON')
