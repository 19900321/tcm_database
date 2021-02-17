import matplotlib.pyplot as plt
import pandas as pd
from math import pi
from process.pyvenn import venn
from process.mysql_setting.connections import query_mysql_pd, save_to_mysql_pd
import asyncio
import pyecharts.options as opts
from pyecharts.charts import Tree


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


def get_herb_properties():
    herb_all_dict = {'etcm': 'herb_info',
                     'symmap': 'smhb',
                     'tcm_herb': 'herb_herb_info',
                     'tcm_id': 'tcm_herb_new',
                     'tcm_mesh': 'herb_info',
                     'tcmid': 'herb_info_detail',
                     'tcmio': 'tcm',
                     'tcmsp': 'new_herb'
                     }

    herb_properties_dict = {}
    for d, v in herb_all_dict.items():
        database_name = d
        table = v
        sql_herb = """SELECT * FROM {};""".format(table)
        pd_result_herb = query_mysql_pd(sql_string=sql_herb, database_name=database_name)
        herb_properties_dict[d] = list(pd_result_herb.columns)

    return herb_properties_dict


def get_herb_overlap():

    herb_all_dict = {'etcm': ('herb_info', 'Herb Name in Chinese'),
                     'symmap': ('smhb', 'Chinese_name'),
                     'tcm_herb': ('herb_herb_info', 'Herb_cn_name'),
                     'tcm_id': ('tcm_herb_new', '中文名'),
                     'tcmid': ('herb_info_detail', 'Chinese Name'),
                     'tcmio': ('tcm', 'chinese_name'),
                     'tcmsp': ('new_herb', 'tcmsp_herb_cn_name')
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
                     'tcm_mesh': ('tcm_compounds', 'CAN string'),
                     'tcmid': ('ingredients_info', 'cid', 'smiles'),
                     'tcmio': ('ingredient', 'smiles', 'inchi', 'inchikey'),
                     'tcmsp': ('new_molecular_info',
                               'tcmsp_ingredient_pubChem_Cid',
                               'tcmsp_ingredient_inchikey',
                               'tcmsp_ingredient_isosmiles')
                     }

    ingre_properties_dict = {}
    for d, v in ingre_all_dict.items():
        database_name = d
        table = v[0]
        sql_herb = """SELECT * FROM {};""".format(table)
        pd_result_herb = query_mysql_pd(sql_string=sql_herb, database_name=database_name)
        ingre_properties_dict[d] = list(pd_result_herb.columns)

    return ingre_properties_dict


def get_ingredient_overlap():
    database_selelcted = ['etcm', 'symmap', 'tcm_herb', 'tcm_id', 'tcmid', 'tcmsp']
    ingre_all_dict = {'etcm': ('ingredient_info', 'External Link to PubChem'),
                      'symmap': ('smit', 'PubChem_id'),
                      'tcm_herb': ('herb_ingredient_info', 'PubChem_id'),
                      'tcm_id': ('tcm_ingredients_all', 'pubchem_cid', 'canonical_smiles', 'standard_inchi_key'),
                      'tcm_mesh': ('tcm_compounds', 'CAN string'),
                      'tcmid': ('ingredients_info', 'cid', 'smiles'),
                      'tcmio': ('ingredient', 'smiles', 'inchi', 'inchikey'),
                      'tcmsp': ('new_molecular_info',
                                'tcmsp_ingredient_pubChem_Cid',
                                'tcmsp_ingredient_inchikey',
                                'tcmsp_ingredient_isosmiles')
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
            is_expand_and_collapse=True
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove")
        )
            .render("result/figure/radial_tree.html")
    )



def get_target_properties():
    pass

def get_disease_properties():
    pass


def get_herb_ingre_pairs():
    pass
    # return how much herb, how much ingredients

def get_herb_ingre_pairs_overlap():
    #averge overlap rate
    pass

def get_herb_ingre_pairs_correlartion():
    #averge overlap rate
    pass

def ADME_correlation():
    pass

def main():
    # plot_radar_2()
    # get_herb_overlap()
    # herb_pro = get_herb_properties()
    # ingre_pro = get_ingredients_properties()
    # get_ingredient_overlap()
    plot_physical_adme_tree()
