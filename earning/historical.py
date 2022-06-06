# we were using rolepoints before, but now we are using tags
# this was part of how we assigned historical cook
#points_query = """select sum(pp.value) earned, u.full_name, u.username from users_user u join userstories_userstory us on u.id = us.assigned_to_id join userstories_rolepoints rps on rps.user_story_id = us.id join projects_points pp on rps.points_id = pp.id join projects_userstorystatus ps on ps.id = us.status_id where ps.slug in ('done', 'historical') group by u.id order by earned desc"""

