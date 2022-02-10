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
TAIGA_USER = os.environ.get('WC_TAIGA_USER', 'taiga')
TAIGA_PASS = os.environ.get('WC_TAIGA_PASS')


conn = psycopg2.connect("dbname={} user={}".format(TAIGA_DB, TAIGA_USER)
#conn = psycopg2.connect("dbname=taiga user=taiga")

cur = conn.cursor()

cur.execute("Select us.id as story_id, us.subject as subj, u.username as username, us.assigned_to_id as user_id, us.tags, ps.slug as status from  userstories_userstory us join projects_userstorystatus ps on us.status_id = ps.id join users_user u on us.assigned_to_id = u.id where ps.slug in ('done', 'ready-for-web', 'ready-for-mobile')")

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

gdf = df.groupby(['user_id','username'],as_index=False).agg(lambda x : x.sum() if x.dtype in ('float64', 'int', 'int32', 'int64') else ' '.join(x))

import pdb; pdb.set_trace()



# postgres integration

# we were using rolepoints before, but now we are using tags
# this was part of how we assigned historical cook
#points_query = """select sum(pp.value) earned, u.full_name, u.username from users_user u join userstories_userstory us on u.id = us.assigned_to_id join userstories_rolepoints rps on rps.user_story_id = us.id join projects_points pp on rps.points_id = pp.id join projects_userstorystatus ps on ps.id = us.status_id where ps.slug in ('done', 'historical') group by u.id order by earned desc"""

# now we have tags

# get the total pq tags paid on the done tasks

# comptroller pushes button for next step if looks reasonable:

# generate final token assignments, submit to multisig approval

# record accounted for

# need tables for :  points_accounted_for, 
