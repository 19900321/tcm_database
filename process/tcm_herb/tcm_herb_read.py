import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import io
import requests
import os


# read files from local folder
def read_herb_files(path_selected):
    database_dict = {}
    for file in os.listdir(path_selected):
        name = file.split('.')[0]
        data = pd.read_csv(path_selected + file, sep='\t')
        database_dict[name] = data
    return database_dict


def tcm_mesh_save_to_mysql(path_selected):

    ## first open mysql the local host, than create database tcm_herb, than click right to eit sceme, to utf8mb4

    # open the mysql workbench, the panel of local host one
    engine = create_engine('mysql://root:Mqxs320321wyy@localhost/tcm_herb?charset=utf8mb4')
    conn = engine.connect()
    database_dict = read_herb_files(path_selected)
    for k,v in database_dict.items():
        try:
            v.to_sql(name=k, con=conn, if_exists='fail', index=False)
        except:
            continue


def main():
    # download_data()
    database_selected = 'tcm_herb'
    path_selected = 'original_data/{}/'.format(database_selected)
    tcm_mesh_save_to_mysql(path_selected)