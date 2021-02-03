import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import io
import requests
import os

def download_data():
    down_load_links_1 = {
        'gene_disease_associations': 'http://mesh.tcm.microbioinformatics.org/download/gene-disease%20associations.txt',
        'herb_info': 'http://mesh.tcm.microbioinformatics.org/download/herb-info.txt',
        'herb_ingredients': 'http://mesh.tcm.microbioinformatics.org/download/herb-ingredients.txt',
        'protein_gene_links': 'http://mesh.tcm.microbioinformatics.org/download/protein-gene%20links.txt',
        'side_effect': 'http://mesh.tcm.microbioinformatics.org/download/side%20effect.txt',
        'toxicity': 'http://mesh.tcm.microbioinformatics.org/download/toxicity.txt'}

    down_load_links_2 = {
        'chemical_protein_associations': 'http://mesh.tcm.microbioinformatics.org/download/gene%20interactions.txt',
        'gene_interactions': 'http://mesh.tcm.microbioinformatics.org/download/chemical-protein%20associations.txt'}

    for info_name, site in down_load_links_1.items():
        data = pd.read_csv(site, sep='\t')
        data.to_csv('original_data/tcm_mesh/{}.txt'.format(info_name), sep='\t')

    for info_name, site in down_load_links_2.items():
        print(info_name)
        s = requests.get(site).content
        data = pd.read_csv(io.StringIO(s.decode('utf-8')), sep='\t')
        data.to_csv('original_data/tcm_mesh/{}.txt'.format(info_name), sep='\t')

# read files from local folder
def read_tcm_sh_files(path_selected):
    database_dict = {}
    for file in os.listdir(path_selected):
        name = file.split('.')[0]
        if name != 'side_effect':
            data = pd.read_csv(path_selected + file, sep='\t', index_col=0)
        else:
            data = pd.read_csv(path_selected + file, sep=',', index_col=0)
        database_dict[name] = data
    return database_dict



def tcm_mesh_save_to_mysql(path_selected):
    # open the mysql workbench, the panel of local host one
    engine = create_engine('mysql://root:Mqxs320321wyy@localhost/tcm_mesh?charset=utf8mb4')
    conn = engine.connect()
    database_dict = read_tcm_sh_files(path_selected)
    for k,v in database_dict.items():
        try:
            v.to_sql(name=k, con=conn, if_exists='fail', index=False)
        except:
            continue


def main():
    # download_data()
    database_selected = 'tcm_mesh'
    path_selected = 'original_data/{}/'.format(database_selected)
    tcm_mesh_save_to_mysql(path_selected)