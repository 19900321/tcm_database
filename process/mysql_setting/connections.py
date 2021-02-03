import pandas as pd
from sqlalchemy import create_engine
import MySQLdb
import MySQLdb.cursors

def query_mysql_pd(sql_string, database_name):
    db_2 = MySQLdb.connect(host="127.0.0.1", user="yin", passwd="Mqxs320321wyy", db=database_name, charset='utf8mb4',
                           cursorclass=MySQLdb.cursors.DictCursor)
    c = db_2.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    c.execute(sql_string)
    inchey_used_2 = c.fetchall()
    pd_result = pd.DataFrame(list(inchey_used_2))
    db_2.close()
    return pd_result


def save_to_mysql_pd(pd_result, database_name, saved_name):
    engine = create_engine('mysql://root:Mqxs320321wyy@localhost/{}?charset=utf8mb4'.format(database_name))
    conn = engine.connect()
    pd_result.to_sql(name=saved_name, con=conn, if_exists='fail', index=False)
    conn.close()