import pandas as pd
import re
import numpy as np

def prepare_formulae_list(formulae):
    def prepare_one_formulae(formulae_info):
        herb_info = re.split('\), |\)', formulae_info)
        detail_herb = ['&'.join(re.split(' \(|， or |, or |，or ', h)) for h in herb_info]
        return detail_herb

    formulae['Formulae_name_component'] = formulae['Formulae_name_component'].apply(lambda x:prepare_one_formulae(x))
    formulae_2 = formulae.explode('Formulae_name_component',ignore_index=True)
    formulae_2 = formulae_2.join(formulae_2['Formulae_name_component'].str.split('&',
                                                                                 2,
                                                                                 expand=True).rename(columns={0: 'pinyin name',
                                                                                                1: 'chinese name',
                                                                                                2: 'latine name'}))

    # clean the data
    formulae_2 = formulae_2[formulae_2['pinyin name'] != '']
    formulae_2 = formulae_2.join(formulae_2['pinyin name'].str.split(' ', 1, expand=True)).rename(columns={0: 'weight',
                                                                                                           1: 'pinyin'})

    formulae_2.pinyin = np.where(formulae_2.pinyin.isnull(), formulae_2.weight, formulae_2.pinyin)
    return formulae_2

def main():
    formulae = pd.read_excel('data/covid19/informtion.xlsx',
                             sheet_name='Sheet1')
    formulae_2 = prepare_formulae_list(formulae)
    formulae_2.to_csv('result/case/covid 19/formulae_processed.txt')

