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


