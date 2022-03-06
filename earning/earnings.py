"""
Pull latest contributions from taiga, and push somewhere for review

"""
import os
import re
import pandas as pd
import psycopg2

# this script will be run locally on the taiga server, as the taiga user
# we do not open the db port to the world
TAIGA_HOST = os.environ.get('WC_TAIGA_HOST', 'localhost')
TAIGA_DB = os.environ.get('WC_TAIGA_DB', 'taiga')
TAIGA_USER = os.environ.get('WC_TAIGA_USER', 'cook_user')
TAIGA_PASS = os.environ.get('WC_TAIGA_PASS')

db_conn = psycopg2.connect("dbname={} host={} user={} password={}".format(TAIGA_DB, TAIGA_HOST, TAIGA_USER, TAIGA_PASS))
#conn = psycopg2.connect("dbname=taiga user=taiga")

GET_DONE_TAGS = """
    Select us.id as story_id, us.subject as subj, u.username as username, us.assigned_to_id as user_id, us.tags, ps.slug as status from  userstories_userstory us join projects_userstorystatus ps on us.status_id = ps.id join users_user u on us.assigned_to_id = u.id where ps.slug in ('done', 'ready-for-web', 'ready-for-mobile')
    """

def generate_cook_updates():

    cur = db_conn.cursor()
    cur.execute(GET_DONE_TAGS)
    res = cur.fetchall()
    rcook = []
    # first parse tags & add up
    for j in range(0, len(res)):
        cook =  0
        tags = res[j][4]
        for tag in tags:
            m = re.search(r'(\d+)\s*cook', tag, re.IGNORECASE)
            if m:
                for grp in m.groups():
                    cook += int(grp)
        res[j] = list(res[j]) + [cook]


    df = pd.DataFrame(res)
    df.columns = ['story_id', 'subj', 'username', 'user_id', 'tags', 'slug', 'cook']

    # only want these fields for review - what did the user do, to earn the cook
    df = df[['subj', 'username', 'user_id', 'cook']]

    # now group by user
    gdf = df.groupby(['user_id','username'],as_index=False).agg(lambda x : x.sum() if x.dtype in ('float64', 'int', 'int32', 'int64') else ' '.join(x))

    return gdf



