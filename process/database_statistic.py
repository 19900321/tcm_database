import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from process.pyvenn import venn
from process.mysql_setting.connections import query_mysql_pd, save_to_mysql_pd
import asyncio
import pyecharts.options as opts
from pyecharts.charts import Tree
from pyecharts.charts import Sankey


def plot_radar_2():
    def make_spider(row, title, color):
        df_new = df.loc[[row],:].dropna(axis=1)
        # number of variable
        categories = list(df_new.columns)[1:]
        N = len(categories)

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(3, 3, row + 1, polar=True, )

        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories, color='grey', size=8)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks(color="grey", size=8)

        # Ind1
        values = df_new.drop(['DATABASE'], axis=1).values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=color, alpha=0.4)

        # Add a title
        plt.title(title, size=8, y=1.15)

    df = pd.read_csv("result/statistic_database.csv")

    # ------- PART 2: Apply to all individuals
    # initialize the figure
    my_dpi = 300
    plt.figure(figsize=(3000 / my_dpi, 3000 / my_dpi), dpi=my_dpi)

    # Create a color palette:
    my_palette = plt.cm.get_cmap("Set2", len(df.index))

    # Loop to plot

    for row in range(0, 9):
        make_spider(row=row, title=df['DATABASE'][row], color=my_palette(row))

    plt.tight_layout()
    plt.savefig('result/figure/figure.png')


def get_formulae_properties():
    formulae_all_dict = {'etcm': 'formulae_info',
                     'tcm_herb': 'herb_disease_info',
                     'tcm_id': 'formulae_detail',
                     'tcmid': 'prescription',
                     'tcmio': 'prescription'
                     }
    formulae_properties_dict = {}
    formulae_pd_dict = {}
    for d, v in formulae_all_dict.items():
        database_name = d
        table = v
        sql_formu = """SELECT * FROM {};""".format(table)
        pd_result_formu = query_mysql_pd(sql_string=sql_formu, database_name=database_name)
        formulae_pd_dict[d] = pd_result_formu
        formulae_properties_dict[d] = list(pd_result_formu.columns)

    return formulae_properties_dict, formulae_pd_dict


def get_herb_properties():
    herb_all_dict = {'etcm': 'herb_info',
                     'symmap': 'smhb',
                     'tcm_herb': 'herb_herb_info',
                     'tcm_id': 'tcm_herb_new',
                     'tcm_mesh': 'herb_info',
                     'tcmid': 'herb_info_detail',
                     'tcmio': 'tcm',
                     'tcmsp': 'new_herb',
                     'tm_mc': 'herb'
                     }

    herb_properties_dict = {}
    herb_pd_dict = {}
    for d, v in herb_all_dict.items():
        database_name = d
        table = v
        sql_herb = """SELECT * FROM {};""".format(table)
        pd_result_herb = query_mysql_pd(sql_string=sql_herb, database_name=database_name)
        herb_pd_dict[d] = pd_result_herb
        herb_properties_dict[d] = list(pd_result_herb.columns)

    return herb_properties_dict, herb_pd_dict


def get_herb_overlap():

    herb_all_dict = {'etcm': ('herb_info', 'Herb Name in Chinese'),
                     'symmap': ('smhb', 'Chinese_name'),
                     'tcm_herb': ('herb_herb_info', 'Herb_cn_name'),
                     'tcm_id': ('tcm_herb_new', '中文名'),
                     'tcm_mesh': ('herb_info', 'chinese name_processed'),
                     'tcmid': ('herb_info_detail', 'Chinese Name'),
                     'tcmio': ('tcm', 'chinese_name'),
                     'tcmsp': ('new_herb', 'tcmsp_herb_cn_name'),
                     'tm_mc': ('herb', 'CHINESE')
                     }

    database_selelcted = ['etcm', 'symmap', 'tcm_herb', 'tcm_id', 'tcmid', 'tcmsp' ]

    herb_dict = {}
    for d, v in herb_all_dict.items():
        database_name = d
        table, col = v[0], v[1]
        if d in database_selelcted:
            sql_herb = """SELECT * FROM {};""".format(table)
            pd_result_herb = query_mysql_pd(sql_string=sql_herb, database_name=database_name)
            herbs = list(pd_result_herb[col].dropna())
            herb_dict[d] = list(set(herbs))

    labels = venn.get_labels([v for k, v in herb_dict.items()], fill=['number', 'logic'])
    names_sum = [':'.join([k, str(len(v))]) for k, v in herb_dict.items()]
    venn.venn6(labels, names=names_sum)
    # fig.show()
    plt.savefig('result/figure/herb_overlap.png')


def get_ingredients_properties():
    ingre_all_dict = {'etcm': ('ingredient_info', 'External Link to PubChem'),
                     'symmap': ('smit', 'PubChem_id'),
                     'tcm_herb': ('herb_ingredient_info', 'PubChem_id'),
                     'tcm_id': ('tcm_ingredients_all', 'pubchem_cid', 'canonical_smiles', 'standard_inchi_key'),
                     'tcm_mesh': ('tcm_compounds', 'pubchem_id', 'CAN string'),
                     'tcmid': ('ingredients_info', 'cid', 'smiles'),
                     'tcmio': ('ingredient', 'smiles', 'inchi', 'inchikey'),
                     'tcmsp': ('new_molecular_info',
                               'tcmsp_ingredient_pubChem_Cid',
                               'tcmsp_ingredient_inchikey',
                               'tcmsp_ingredient_isosmiles'),
                    'tm_mc': ('ingredient_info', 'CID')
                     }

    ingre_properties_dict = {}
    ingre_pd_dict = {}
    for d, v in ingre_all_dict.items():
        database_name = d
        table = v[0]
        sql_herb = """SELECT * FROM {};""".format(table)
        pd_result_herb = query_mysql_pd(sql_string=sql_herb, database_name=database_name)
        ingre_pd_dict[d] = pd_result_herb
        ingre_properties_dict[d] = list(pd_result_herb.columns)

    return ingre_properties_dict, ingre_pd_dict


def get_ingredient_overlap():
    database_selelcted = ['etcm', 'symmap', 'tcm_herb', 'tcm_id', 'tcmid', 'tcmsp']
    ingre_all_dict = {'etcm': ('ingredient_info', 'External Link to PubChem'),
                      'symmap': ('smit', 'PubChem_id'),
                      'tcm_herb': ('herb_ingredient_info', 'PubChem_id'),
                      'tcm_id': ('tcm_ingredients_all', 'pubchem_cid', 'canonical_smiles', 'standard_inchi_key'),
                      'tcm_mesh': ('tcm_compounds', 'pubchem_id', 'CAN string'),
                      'tcmid': ('ingredients_info', 'cid', 'smiles'),
                      'tcmio': ('ingredient', 'smiles', 'inchi', 'inchikey'),
                      'tcmsp': ('new_molecular_info',
                                'tcmsp_ingredient_pubChem_Cid',
                                'tcmsp_ingredient_inchikey',
                                'tcmsp_ingredient_isosmiles'),
                      'tm_mc': ('ingredient_info', 'CID')
                      }
    ingre_dict = {}
    for d, v in ingre_all_dict.items():
        database_name = d
        table, col = v[0], v[1]
        if d in database_selelcted:
            sql_ingre = """SELECT * FROM {};""".format(table)
            pd_result_herb = query_mysql_pd(sql_string=sql_ingre, database_name=database_name)
            pd_result_herb = pd_result_herb[~pd_result_herb[col].isin(['Not Available', ''])]
            ingredients = list(pd_result_herb[col].dropna().astype(int))
            ingre_dict[d] = list(set(ingredients))

    labels = venn.get_labels([v for k, v in ingre_dict.items()], fill=['number', 'logic'])
    names_sum = [':'.join([k, str(len(v))]) for k, v in ingre_dict.items()]
    venn.venn6(labels, names=names_sum)
    # fig.show()
    plt.savefig('result/figure/ingre_overlap.png')


def get_adme_properties():
    ingre_pro = get_ingredients_properties()
    clean_tree_list = []
    for d, p in ingre_pro.items():
        print(d)
        if d == 'tcmsp':
            p = [p_i[17:] for p_i in p]
        if d == 'etcm':
            p = [p_i if 'ADMET' not in p_i else p_i[5] for p_i in p]
        clean_tree_list.append({d: detect_annotation(p)})
    return d


def detect_annotation(pro_list):
    structure = ['struc', 'smil', ' formula', 'can', 'inchi']
    annotation = ['name', 'alia', 'synony']
    links = ['_id', 'pubchem', 'cid', 'chem', 'cas']
    term_dict = {'structure': structure,
                 'annotation': annotation,
                 'links': links,
                 'ADMET': structure+annotation+links}

    child_dict = []
    for type_term, terms in term_dict.items():
        type_term_list = []
        if type_term != 'ADMET':
            for p in pro_list:
                if any(t in p.lower() for t in terms):
                    type_term_list.append({'name': p.capitalize()})
        else:
            for p in pro_list:
                if all(t not in p.lower() for t in terms):
                    type_term_list.append({'name': p.capitalize()})

        child_dict.append({"children": type_term_list, 'name': type_term})

    return child_dict


def plot_physical_adme_tree():
    ingre_pro = get_ingredients_properties()

    clean_tree_list = []
    for d, p in ingre_pro.items():
        print(d)
        if d == 'tcmsp':
            p = [p_i[17:] for p_i in p]
        if d == 'etcm':
            p = [p_i if 'ADMET' not in p_i else p_i[5] for p_i in p ]
        clean_tree_list.append({"children": detect_annotation(p), 'name': d})
    data = {"children": clean_tree_list, 'name': 'TCM_database'}

    (
        Tree(init_opts=opts.InitOpts(width="2000px", height="1200px"))
            .add(
            series_name="",
            data=[data],
            pos_top='18%',
            pos_bottom='14%',
            layout='radial',
            symbol='emptyCircle',
            symbol_size=7,
            initial_tree_depth=4,
            is_expand_and_collapse=True,
            label_opts=opts.LabelOpts(position="left"),
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove")
        )
            .render("result/figure/radial_tree.html")
    )


def get_target_properties():
    target_all_dict = {'etcm': 'herb_target',
                         'symmap': 'smtt',
                         'tcm_herb': 'herb_target_info',
                         'tcm_id': 'cp_targets',
                         'tcm_mesh': 'protein_gene_links',
                         'tcmid': 'stitch_interaction_all',
                         'tcmio': 'target',
                         'tcmsp': 'info_targets'
                         }

    target_properties_dict = {}
    target_pd_dict = {}
    for d, v in target_all_dict.items():
        database_name = d
        table = v
        sql_target = """SELECT * FROM {};""".format(table)
        pd_result_target = query_mysql_pd(sql_string=sql_target, database_name=database_name)
        target_pd_dict[d] = pd_result_target
        target_properties_dict[d] = list(pd_result_target.columns)
    return target_properties_dict, target_pd_dict


def plot_db_links():
    node_pd = pd.read_excel('result/relationship.xlsx', sheet_name='sy_nodes')
    nodes = [{i: j} for i, j in zip(node_pd['type'], node_pd['db'])]

    link_pd = pd.read_excel('result/relationship.xlsx', sheet_name='sy_links')
    links =link_pd.to_dict('records')

    c = (
        Sankey(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add(
            "sankey",
            nodes,
            links,
            pos_left="22%",
            pos_top="10%",
            focus_node_adjacency=True,
            itemstyle_opts=opts.ItemStyleOpts(border_width=0.2, border_color="black"),
            linestyle_opt=opts.LineStyleOpts(color='source', curve=0.1, opacity=0.2),
            tooltip_opts=opts.TooltipOpts(trigger_on="mousemove"),
            label_opts=opts.LabelOpts(position="left"),

        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Sankey Diagram of database links"))
            .render("result/figure/sankey_database.html")
    )


def get_herb_ingre_pairs():
    h_i_all_dict = {
        'etcm': 'herb_ingredient',
        'symmap': 'smit_smhb',
        'tcm_id': 'tcm_plant_ingredient_pairs_allingredients',
        'tcm_mesh': 'herb_ingredients',
        'tcmid': 'herb_ingre_new',
        'tcmsp': 'herbs_molecules_relationships',
        'tm_mc': 'herb_ingredient_info'
    }

    h_i_pd_dict = {}

    for d, v in h_i_all_dict.items():
        database_name = d
        table = v
        sql_h_i = """SELECT * FROM {};""".format(table)
        pd_result_h_i = query_mysql_pd(sql_string=sql_h_i, database_name=database_name)
        if d == 'tcmsp':
            pd_result_h_i = pd_result_h_i.drop(columns='tcmsp_herb_cn_name')
        h_i_pd_dict[d] = pd_result_h_i
    return h_i_pd_dict


def get_herb_ingre_pairs_detail():

    herb_all_dict = {'etcm': ('herb_info', 'Herb Name in Chinese'),
                     'symmap': ('smhb', 'Chinese_name'),
                     'tcm_herb': ('herb_herb_info', 'Herb_cn_name'),
                     'tcm_id': ('tcm_herb_new', '中文名'),
                     'tcm_mesh': ('herb_info', 'chinese name_processed'),
                     'tcmid': ('herb_info_detail', 'Chinese Name'),
                     'tcmio': ('tcm', 'chinese_name'),
                     'tcmsp': ('new_herb', 'tcmsp_herb_cn_name'),
                     'tm_mc': ('herb', 'CHINESE')
                     }


    ingre_all_dict = {'etcm': ('ingredient_info', 'External Link to PubChem'),
                      'symmap': ('smit', 'PubChem_id'),
                      'tcm_herb': ('herb_ingredient_info', 'PubChem_id'),
                      'tcm_id': ('tcm_ingredients_all', 'pubchem_cid', 'canonical_smiles', 'standard_inchi_key'),
                      'tcm_mesh': ('tcm_compounds', 'pubchem_id', 'CAN string'),
                      'tcmid': ('ingredients_info', 'cid', 'smiles'),
                      'tcmio': ('ingredient', 'smiles', 'inchi', 'inchikey'),
                      'tcmsp': ('new_molecular_info',
                                'tcmsp_ingredient_pubChem_Cid',
                                'tcmsp_ingredient_inchikey',
                                'tcmsp_ingredient_isosmiles'),
                      'tm_mc': ('ingredient_info', 'CID')
                      }

    herb_ingre_all_dict = {
                    'etcm': {'table': 'herb_ingredient',
                            'herb': 'herb_id',
                            'herb_ingre': {'herb': 'herb_id',
                                           'ingre': 'ingre_id'},
                            'ingre': 'Ingredient_id'
                             },
                     'symmap': {'table': 'smit_smhb',
                                'herb': 'Herb_id',
                                'herb_ingre': {'herb': 'Herb_id',
                                               'ingre': 'MOL_id'},
                                'ingre': 'MOL_id'
                                },
                     'tcm_id': {
                             'whole_table': 'tcm_plant_ingredient_pairs_allingredients'
                                },
                     'tcm_mesh': {'table': 'herb_ingredients',
                                    'herb': 'pinyin name',
                                    'herb_ingre': {'herb': 'herb',
                                                   'ingre': 'pubchem_id'},
                                    'ingre': 'pubchem_id'
                                  },
                     'tcmid':  {'whole_table': 'herb_ingre_new'
                                },
                     'tcmsp': {'table': 'herbs_molecules_relationships',
                                'herb': 'tcmsp_herb_id',
                                'herb_ingre': {'herb': 'tcmsp_herb_id',
                                               'ingre': 'tcmsp_ingredient_id'
                                               },
                                'ingre': 'tcmsp_ingredient_id'},
                    'tm_mc': {'whole_table': 'herb_ingredient_info'
                              }
                    }

    database_selelcted = ['etcm', 'symmap', 'tcm_herb', 'tcm_id', 'tcmid', 'tcmsp']
    herb_ingre_pd = get_herb_ingre_pairs()
    herb_pro, herb_pd = get_herb_properties()
    ingre_pro, ingre_pd = get_ingredients_properties()

    herb_ingre_result_dict = {}
    for d in herb_ingre_all_dict.keys():
        print(d)
        herb_to_col = herb_all_dict[d][1]
        ingre_to_col = ingre_all_dict[d][1]
        if 'whole_table' in herb_ingre_all_dict[d]:
            pair_pd_all = herb_ingre_pd[d]
        else:
            h_i_pd = herb_ingre_pd[d]
            # prepare the herb pd
            def pre_single_pd(h_i_pd, single_data_pd, data_to_col, herb_ingre_all_dict, type ):
                data_pd_one = single_data_pd[d]
                data_pd_one = data_pd_one.astype(str)
                data_pd_key_col = herb_ingre_all_dict[d][type]
                data_ingre_h_key_col = herb_ingre_all_dict[d]['herb_ingre'][type]

                data_pd_one = data_pd_one.dropna(how='any',
                                                 subset=[data_pd_key_col, data_to_col],
                                                 axis=0).drop_duplicates()
                if 'id' in data_ingre_h_key_col and d != 'tcmsp':
                    h_i_pd[data_ingre_h_key_col] = h_i_pd[data_ingre_h_key_col].astype(int)
                elif d == 'tcmsp':
                    h_i_pd[data_ingre_h_key_col] = h_i_pd[data_ingre_h_key_col].astype(str)

                if 'id' in data_pd_key_col and d != 'tcmsp':
                    data_pd_one[data_pd_key_col] = data_pd_one[data_pd_key_col].astype(int)
                elif d == 'tcmsp':
                    data_pd_one[data_pd_key_col] = data_pd_one[data_pd_key_col].astype(str)


                pair_pd_all = pd.merge(h_i_pd,
                                       data_pd_one,
                                       left_on=data_ingre_h_key_col,
                                       right_on=data_pd_key_col,
                                       how='left')
                return pair_pd_all

            pair_pd_all = pre_single_pd(h_i_pd, herb_pd, herb_to_col, herb_ingre_all_dict, 'herb')
            pair_pd_all = pre_single_pd(pair_pd_all, ingre_pd, ingre_to_col, herb_ingre_all_dict, 'ingre')
            #save_to_mysql_pd(pair_pd_all, database_name=d, saved_name='all_herb_ingre_detail')

        pair_pd_all = pair_pd_all[~pair_pd_all[ingre_to_col].isin([None, 'nan', '', np.nan, 'Not Available', 'None'])]
        pair_pd_all = pair_pd_all[~pair_pd_all[herb_to_col].isin([None, 'nan', '', np.nan, 'Not Available', 'None'])]
        pair_pd_all = pair_pd_all[pair_pd_all[ingre_to_col].notnull()]
        pair_pd_all = pair_pd_all[pair_pd_all[herb_to_col].notnull()]
        pair_pd_all[ingre_to_col] = pair_pd_all[ingre_to_col].astype(float).astype(int)
        pair_pd_all = pair_pd_all[[herb_to_col, ingre_to_col]].drop_duplicates()
        pair_dict = dict(pair_pd_all.groupby(herb_to_col)[ingre_to_col].apply(list))
        herb_ingre_result_dict[d] = pair_dict
        #herb_ingre_result_dict[d] = pair_pd_all
    return herb_ingre_result_dict


def get_herb_ingre_pairs_correlartion():
    herb_ingre_china_cid = pickle.load(open('result/herb_ingre_china_cid.dict', 'rb'))
    databases = list(herb_ingre_china_cid.keys())


    def herb_cor(overlap_herb, d_1, d_2, herb_ingre_china_cid):
        jacard = []
        for h in overlap_herb:
            union_l = len(set(herb_ingre_china_cid[d_1][h]) & set(herb_ingre_china_cid[d_2][h]))
            over = len(set(herb_ingre_china_cid[d_1][h]) | set(herb_ingre_china_cid[d_2][h]))
            jacard.append(union_l/over)
        return np.mean(jacard)

    cor_pd = pd.DataFrame(columns=databases, index=databases)
    for d_1 in databases:
        for d_2 in databases:
            overlap_herb = set(herb_ingre_china_cid[d_1]) & set(herb_ingre_china_cid[d_2])
            jaccard = herb_cor(overlap_herb, d_1, d_2, herb_ingre_china_cid)
            cor_pd.loc[d_1, d_2] = jaccard

    cor_pd = cor_pd.astype(float)
    mask = np.triu(np.ones_like(cor_pd, dtype=np.bool))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    plt.figure(figsize=(8,8))
    ax = sns.heatmap(cor_pd,
                annot=True,
                mask=mask,
                linewidths=.5,
                cmap=cmap,
                square=True,
                cbar_kws=dict(use_gridspec=False,
                              shrink=.7,
                              location='right'),
                cbar=True
            )

    #plt.show()
    plt.savefig('result/figure/herb_ingre.png')







def ADME_correlation():
    pass


def main():
    # plot_radar_2()
    # get_herb_overlap()
    # formulae_properties_dict, formulae_pd_dict = get_formulae_properties()
    # herb_pro, herb_pd = get_herb_properties()
    # ingre_pro, ingre_pd = get_ingredients_properties()
    # target_pro, target_pd = get_target_properties()
    # get_ingredient_overlap()
    # plot_physical_adme_tree()
    # plot_db_links()
    herb_ingre_result_dict = get_herb_ingre_pairs_detail()
    pickle.dump(herb_ingre_result_dict, open('result/herb_ingre_china_cid.dict', 'wb'))
    herb_ingre_china_cid  = pickle.load(open('result/herb_ingre_china_cid.dict', 'rb'))
    return herb_ingre_result_dict
