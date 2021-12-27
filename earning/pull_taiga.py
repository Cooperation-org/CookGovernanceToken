"""
Pull latest contributions from taiga, and push somewhere for review

"""

# postgres integration

points_query = """select sum(pp.value) earned, u.full_name, u.username from users_user u join userstories_userstory us on u.id = us.assigned_to_id join userstories_rolepoints rps on rps.user_story_id = us.id join projects_points pp on rps.points_id = pp.id join projects_userstorystatus ps on ps.id = us.status_id where ps.slug in ('done', 'historical') group by u.id order by earned desc"""

# later remove historical

# query points (done tasks only) that are not already accounted for

# get the total pq tags paid on the done tasks

# publish the points and the points * salaries - paid for for equity, points * salaries for governance
# or maybe no salaries!  maybe just assign points at the meetings regardless?  

# encourage people to update taiga

# recalculate after taiga updates

# comptroller pushes button for next step if looks reasonable:

# generate final token assignments, submit to multisig approval

# record accounted for

# need tables for :  points_accounted_for, 
