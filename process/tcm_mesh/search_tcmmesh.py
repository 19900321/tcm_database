import pandas as pd
from process.mysql_setting.connections import query_mysql_pd, save_to_mysql_pd


def get_herb_ingredient_tcmsp(herb_pinyin_list):
    database_name = 'tcm_mesh'
    herb_list_str = ','.join(["'{}'".format(x) for x in set(herb_pinyin_list)])
    sql = """SELECT * FROM herb_info as h,
            herb_ingredients as h_m,
            compounds as m
            where h.`pinyin name` in ({})
            and h.`pinyin name` = h_m.herb
            and m.chemical = h_m.chemical
            ;
            """.format(herb_list_str)
    pd_result = query_mysql_pd(sql_string=sql, database_name=database_name)

    return pd_result


def get_ingre_tar_tcmsp(ingredient_id_list):
    database_name = 'tcm_mesh'
    ingredient_id_str = ','.join(["'{}'".format(x) for x in set(ingredient_id_list)])
    sql = """SELECT * FROM 
            chemical_protein_associations as m_t
            where m_t.chemical in ({})
            ;""".format(ingredient_id_str)
    pd_result = query_mysql_pd(sql_string=sql, database_name=database_name)

    return pd_result


def get_side_toxi_effect(ingredient_id_list):
    database_name = 'tcm_mesh'
    ingredient_id_str = ','.join(["'{}'".format(x) for x in set(ingredient_id_list)])
    sql = """SELECT * FROM 
            side_effect as side
            where side.chemical in ({});""".format(ingredient_id_str)

    pd_result_side = query_mysql_pd(sql_string=sql, database_name=database_name)

    return pd_result_side


def get_toxicity(name_list):
    database_name = 'tcm_mesh'
    name_list_str = ','.join(["'{}'".format(x) for x in set(name_list)])
    sql_toxi = """SELECT * FROM 
                    tcm_mesh.toxicity as toxi
                    where toxi.name in ({});""".format(name_list_str)

    pd_result_toxi = query_mysql_pd(sql_string=sql_toxi, database_name=database_name)

    return pd_result_toxi