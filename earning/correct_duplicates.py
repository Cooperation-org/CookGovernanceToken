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


def find_and_fix_dupes():

    cur = db_conn.cursor()
    cur.execute("select * from pending_cook")
    res = cur.fetchall()
    rcook = []
    # remove dupes and correct the totals
    for j in range(0, len(res)):
        user_id = res[j][0]
        cook =  res[j][1]
        org_cook = cook
        tasks = res[j][2]
        new_tasks = []
        for task in tasks:
            if task in new_tasks:
                # its a dupe, calculate its tags and subtract from the total
                cur.execute("select tags from userstories_userstory where id = {}".format(task))
                tags = cur.fetchone()[0]
                tag_cook = 0
                for tag in tags:
                    m = re.search(r'(\d+)\s*cook', tag, re.IGNORECASE)
                    if m:
                        for grp in m.groups():
                            tag_cook += int(grp)
                # subtract from the total
                cook = cook - tag_cook
            else:
                new_tasks.append(task)

        if cook != org_cook:
            fix_q = 'update pending_cook set cook = {}, tasks = ARRAY{} where user_id = {}'.format(cook, new_tasks, user_id)
            print("Would perform update: {}".format(fix_q))
            import pdb; pdb.set_trace()
            cur.execute(fix_q)
    cur.connection.commit()

find_and_fix_dupes()
