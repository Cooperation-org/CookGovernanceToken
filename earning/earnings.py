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
    Select CAST(us.id as VARCHAR) as story_id, us.subject as subj, u.username as username, us.assigned_to_id as user_id, us.tags, ps.slug as status from  userstories_userstory us join projects_userstorystatus ps on us.status_id = ps.id join users_user u on us.assigned_to_id = u.id where ps.slug  = 'done' and us.tags @> ARRAY['pq']
    """
    # for now only include ones already marked pq; later we will add up $ as well as cook
    # for now do not include ready-for-web or ready-for-mobile

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
    df = df[['subj', 'story_id', 'username', 'user_id', 'cook']]

    # now group by user
    gdf = df.groupby(['user_id','username'],as_index=False).agg(lambda x : x.sum() if x.dtype in ('float64', 'int', 'int32', 'int64') else ';'.join(x))

    # add a "adjustment" column for admin use
    gdf['adjustment'] = ''

    return gdf


def record_pending_cook(df):
    """
    accept df, record totals in pending
    move associated tasks to historical
    Do these steps atomically
    """

    # we expect fields of
    # Id, Handle, Task titles, Task IDs, earned COOK, adjustment
    # these are from the google sheet header row
    # we should establish these as constants for creating next sheet
    # they must be human readable
    cur = db_conn.cursor()

    # we can loop thru should be no more than 50 rows
    # don't commit til everything is done

    for row in df.to_numpy().tolist()[1:]:  # first row is header
        (user_id_str, handle, titles, task_ids, earned_cook, adjustment) = row[0:6]
        if adjustment == '':
            adjustment = 0
        if earned_cook == '':
            earned_cook = 0
        pending_cook_to_add = int(earned_cook) + int(adjustment)
        if user_id_str == '':
            continue
        user_id = int(user_id_str)
        task_ids = re.sub(';', ',', task_ids)

        update_q = """Insert into pending_cook as pc (user_id, cook, tasks)
                    values ({}, {}, ARRAY[{}])
                    on conflict (user_id) do
                        update set 
                        cook = pc.cook + {},
                        tasks = array_cat(pc.tasks, ARRAY[{}])
                        where pc.user_id = {}""".format(
            user_id, pending_cook_to_add, task_ids,
            pending_cook_to_add, task_ids, user_id)

        cur.execute(update_q)

        # move to status historical
        historical_q = "update userstories_userstory us set status_id = (select id from projects_userstorystatus where project_id = us.project_id and slug = 'historical') where id in ({})".format(task_ids)

        cur.execute(historical_q)

    cur.connection.commit()


