
import pandas as pd
def get_basic_info():
    # defining the html contents of a URL.
    df = pd.read_html('http://bidd.group/CMAUP/browsemedplant.php')
    df[0].to_csv('original_data/cmaup/plant_info.txt', sep='\t')
    df_d = pd.read_html('http://bidd.group/CMAUP/browseplantbydis.php')
    df_d[0].to_csv('original_data/cmaup/disease_info.txt', sep='\t')