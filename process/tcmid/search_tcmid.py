import pandas as pd
from process.mysql_setting.connections import query_mysql_pd, save_to_mysql_pd


def get_herb_ingredient_tcmsp(herb_list):
    database_name = 'tcmid'
    herb_list_str = ','.join(["'{}'".format(x) for x in set(herb_list)])
    sql = """SELECT * FROM new_herb as h,
            new_molecular_info as m,
            info_targets as t, 
            herbs_molecules_relationships as h_m
            where h.tcmsp_herb_cn_name in ({})
            and h.tcmsp_herb_id = h_m.tcmsp_herb_id
            and m.tcmsp_ingredient_id = h_m.tcmsp_ingredient_id
            ;
            """.format(herb_list_str)
    pd_result = query_mysql_pd(sql_string=sql, database_name=database_name)

    return pd_result


def get_ingre_tar_tcmid_stitch(ingredient_id_list):
    database_name = 'tcmid'
    ingredient_id_str = ','.join(["'{}'".format(x) for x in set(ingredient_id_list)])
    sql = """SELECT * FROM ingre_new as m,
                stitch_interaction_all as m_t
                where m.`Ingredient id` = ({})
                and m.Stitch_cid_m = m_t.stitch_id;""".format(ingredient_id_str)
    pd_result = query_mysql_pd(sql_string=sql, database_name=database_name)
    return pd_result


def get_ingre_tar_tcmid(ingredient_id_list):
    database_name = 'tcmid'
    ingredient_id_str = ','.join(["'{}'".format(x) for x in set(ingredient_id_list)])
    sql = """SELECT * FROM ingre_new as m,
                    ingredient_targets_disease_drug as m_t
                    where m.`Ingredient id` = ({})
                    and m.`Ingredient id` = m_t.`Ingredient id`;""".format(ingredient_id_str)
    pd_result = query_mysql_pd(sql_string=sql, database_name=database_name)

    return pd_result