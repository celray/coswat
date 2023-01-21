#!/bin/python3

from cjfx import *
ignore_warnings()

# change working directory
me = os.path.realpath(__file__)
os.chdir(os.path.dirname(me))

models_dir =       "../../../../tools/CoSWAT-Global-Model/model-setup/CoSWATv0.2.2"
zones = list_folders(models_dir)

for model_setup in zones:
    parts       = model_setup.split('-')

    continent   = parts[0]
    basin       = parts[1]

    print(f"\t# copying {basin}")

    create_path(f'../model-setups/{continent}/{basin}/vectors/')

    lsus2 = geopandas.read_file(f"{models_dir}/{model_setup}/Watershed/Shapes/lsus2.shp")
    hrus2 = geopandas.read_file(f"{models_dir}/{model_setup}/Watershed/Shapes/hrus2.shp")
    rivs1 = geopandas.read_file(f"{models_dir}/{model_setup}/Watershed/Shapes/rivs1.shp")
    
    lsus2.to_file(f'../model-setups/{continent}/{basin}/vectors/lsus2.gpkg', driver = "GPKG")
    hrus2.to_file(f'../model-setups/{continent}/{basin}/vectors/hrus2.gpkg', driver = "GPKG")
    rivs1.to_file(f'../model-setups/{continent}/{basin}/vectors/rivs1.gpkg', driver = "GPKG")

    files = list_files(f"{models_dir}/{model_setup}/Scenarios/Default/TxtInOut/")
    model_files = []
    
    for fn in files:
        if fn.endswith('.txt') or fn.endswith('.txt'):
            continue
    
        model_files.append(fn)
    
    counter = 0
    end = len(model_files)
    for fn in model_files:

        counter += 1
        copy_file(fn, f'../model-setups/{continent}/{basin}/txtinout/{file_name(fn)}', v = False)

        show_progress(counter, end, string_after = f'copying {file_name(fn)}...     ')
    
    print('\n')
