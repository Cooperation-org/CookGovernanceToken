# How to process earnings

1) ssh to taiga.whatscookin.us (see vault for credentials)

2) Run the dashboard
```
cd ~/GovernanceToken/earning
python3 dashboard.py
```

3) visit the dashboard: https://taiga.whatscookin.us/dash

3.1) Review the cook earnings and adjust as appropriate, if people did not record (later this should be by task and require oversight)
3.2) Approve & Post

The totals should now be recorded in the taiga table `pending_cook` and the recorded tasks should now be moved into the state 'historical'

-- the following steps are currently manual --

4) `copy (select p.user_id, p.cook, u.email from pending_cook p join users_user u on p.user_id = u.id) to '/tmp/export.csv';`

5) upload this to gnosis safe and fairmint

6) move `pending_cook` to `posted_cook`

-- one time only, for the first upload: --

4.1) Download `/tmp/export.csv` ; download [Total Sum of COOK with emails](https://docs.google.com/spreadsheets/d/1Akq2c1ywZWZmK02lLIYM4QX2ajw9IWVOB5ODR4UmpiA/edit#gid=0)

4.2) Use pandas to merge based on email to add a column to the total sum spreadsheet for the update


