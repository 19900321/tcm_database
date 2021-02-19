from process.symmap import symmap_read
from process.etcm import etcm_read
from process import database_statistic

if __name__ == '__main__':
    # tcmsp_read.main()
    # tcm_id_read.main()
    # tcm_mesh_read.main()
    # tcm_herb_read.main()
    # symmap_read.main()
    # etcm_read.main()
    herb_ingre_result_dict = database_statistic.main()


