import pickle
import pandas as pd
from process.mysql_setting.connections import save_to_mysql_pd


def prepare_simple_info(herb_dict, type):
    simple_herb_dict = {k: {k2: v2 for k2, v2 in v.items() if isinstance(v2, str) }
                        for k, v in herb_dict.items()
                        if k != 0}
    if type == 'Ingredient':
        simple_herb_dict = {k: {k2: v2 for k2, v2 in v.items() if k2 != 'Herbs Containing This Ingredient' and k2 != 'Formulas Containing This Ingredient'}
                            for k, v in simple_herb_dict.items()
                            if k != 0}

    herb_info = pd.DataFrame.from_dict(simple_herb_dict, orient='index').reset_index()
    herb_info = herb_info.rename(columns={'index': '{}_id'.format(type)})
    save_to_mysql_pd(pd_result=herb_info, database_name='etcm', saved_name='{}_info'.format(type))


def prepare_list(herb_dict, type):
    name_dict = {'Candidate Target Genes': '{}_target'.format(type),
                 'Diseases Associated with This {}'.format(type): '{}_disease'.format(type)
                 }

    for term in ['Candidate Target Genes', 'Diseases Associated with This {}'.format(type)]:
        term_dict = {k: {k2: v2 for k2, v2 in v.items() if k2 == term}
                     for k, v in herb_dict.items()}
        info_pd = pd.DataFrame.from_dict(term_dict, orient='index').reset_index()
        info_pd = info_pd.rename(columns={'index': '{}_id'.format(type)})
        info_pd = info_pd.explode(column=term)

        save_to_mysql_pd(pd_result=info_pd, database_name='etcm', saved_name=name_dict[term])


def prepare_dictionary(herb_dict, type):
    name_dict = {
        'go_dict': '{}_go'.format(type),
        'pathways_dict': '{}_pathways'.format(type),
        'Components': '{}_ingredient'.format(type),
        'Herbs Contained in This {} (Chinese)'.format(type): '{}_herb_china'.format(type),
        'Herbs Contained in This {} (Chinese Pinyin)'.format(type): '{}_herb_pinyin'.format(type)
    }

    terms_list = ['Herbs Contained in This {} (Chinese)'.format(type),
                  'Herbs Contained in This {} (Chinese Pinyin)'.format(type)]
    for term in list(name_dict.keys()):
        result_pd_all = []
        for k, v in herb_dict.items():
            if term in list(v.keys()):
                if v[term] != None :
                    v2_dict = {i: v2 for i, v2 in enumerate(list(v[term]))}
                    result_pd = pd.DataFrame.from_dict(v2_dict, orient='index')
                    result_pd.insert(0, '{}_id'.format(type), k)
                    result_pd_all.append(result_pd)
        result_pd_all = pd.concat(result_pd_all, axis=0)
        save_to_mysql_pd(pd_result=result_pd_all, database_name='etcm', saved_name=name_dict[term])


def prepare_herb_ingredient(herb_dict):
    result_pd_all = []
    for k, v in herb_dict.items():
        ingre_target_list = v['Components']
        ingre_name_id = {i['ingre_name']: i['ingre_id'] for i in ingre_target_list}

        herb_target_pd = v['ingre_target']
        herb_target_pd['ingre_id'] = herb_target_pd['Chemical Component'].apply(lambda x: ingre_name_id.get(x))
        herb_target_pd = herb_target_pd.dropna()
        result_pd_all.append(herb_target_pd)

    result_pd_all = pd.concat(result_pd_all, axis=0)
    result_pd_all = result_pd_all.drop_duplicates(keep='first')

    result_pd_all['Candidate Target genes'] = result_pd_all['Candidate Target genes'].apply(lambda x: x.split(','))
    result_pd_all = result_pd_all.explode(column='Candidate Target genes')
    save_to_mysql_pd(pd_result=result_pd_all, database_name='etcm', saved_name='herb_ingredient_target')


def prepare_herb_pd(herb_dict):
    type = 'Herb'
    prepare_simple_info(herb_dict, type)
    prepare_list(herb_dict, type)
    prepare_dictionary(herb_dict, type)
    prepare_herb_ingredient(herb_dict)

def prepare_formulae_pd(formula_dict):
    type = 'Formula'
    prepare_simple_info(formula_dict, type)
    prepare_list(formula_dict, type)
    prepare_dictionary(formula_dict, type)


def prepare_ingredient(ingre_dict):

    type = 'Ingredient'
    prepare_simple_info(ingre_dict, type)


def main():
    herb_dict = pickle.load(open('processed_data/etcm_herb_dict', 'rb'))
    formula_dict = pickle.load(open('processed_data/etcm_formulae_dict', 'rb'))
    ingre_dict = pickle.load( open('processed_data/etcm_ingre_dict', 'rb'))