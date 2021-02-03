
import pandas as pd
from process.mysql_setting.connections import query_mysql_pd, save_to_mysql_pd

def get_key_values():

    """SELECT
    count(*)
    FROM
    tcmsp.molecules_targets_relationships;"""

    """SELECT
    count(distinct(tcmsp_ingredient_id))
    FROM
    tcmsp.molecules_targets_relationships;"""

    """SELECT
    count(distinct(tcmsp_target_id))
    FROM
    tcmsp.molecules_targets_relationships;"""

    """SELECT
    count(*)
    FROM
    tcmsp.herbs_molecules_relationships;"""

    """SELECT
    count(distinct(tcmsp_herb_id))
    FROM
    tcmsp.herbs_molecules_relationships;"""

    """SELECT
    count(distinct(tcmsp_ingredient_id))
    FROM
    tcmsp.herbs_molecules_relationships;"""


def get_herb_ingredient_tcmsp(herb_list):
    database_name = 'tcmsp'
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


def get_ingre_tar_tcmsp(ingredient_id_list):
    database_name = 'tcmsp'
    ingredient_id_str = ','.join(["'{}'".format(x) for x in set(ingredient_id_list)])
    sql = """SELECT * FROM new_molecular_info as m,
            info_targets as t,
            molecules_targets_relationships as m_t
            where m.tcmsp_ingredient_id in ({})
            and m_t.tcmsp_ingredient_id = m.tcmsp_ingredient_id
            and m_t.tcmsp_target_id = t.tcmsp_target_id;""".format(ingredient_id_str)
    pd_result = query_mysql_pd(sql_string=sql, database_name=database_name)

    return pd_result

