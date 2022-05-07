import os
import pygsheets
import pandas as pd

SHEETS_API_KEY = os.environ.get('WC_SHEETS_API_KEY') # unused actually
SERVICE_FILE = '/home/ubuntu/GovernanceToken/earning/gcsheets.json'

COOK_SHEET = 'https://docs.google.com/spreadsheets/d/1XcN1FoWoco9OQy6OwjOYmVRgF88VlNNphrfiADARJUY'


gc = pygsheets.authorize(service_file=SERVICE_FILE)

def push_to_sheet(df):

    rows = df.to_numpy().tolist()

    #open the google spreadsheet
    sh = gc.open_by_url(COOK_SHEET)

    #select the first sheet
    wks = sh[0]

    #update the first sheet with df, starting at cell B2.
    wks.update_values(crange='A2',values = rows)

    return COOK_SHEET


def pull_from_sheet():

    #open the google spreadsheet
    sh = gc.open_by_url(COOK_SHEET)

    wks = sh[0]
    rows = wks.get_all_values()

    df = pd.DataFrame(rows)

    return df

def move_sheet_to_processed():
    #open the google spreadsheet
    sh = gc.open_by_url(COOK_SHEET)

    #TODO
    # update index to move sheet to second position
    """
    https://stackoverflow.com/questions/42004124/move-a-sheet-to-a-particular-position-using-python-the-google-sheets-api
reqs = {'requests': [
    # reorder sheet4 to index 2
    {'updateSheetProperties': {
        'properties': {
            'sheetId': sheet['properties']['sheetId'],
            'index': 2
        }
    }}
]}
SHEETS.spreadsheets().batchUpdate(
    spreadsheetId=FILE_ID, body=reqs).execute()

https://pygsheets.readthedocs.io/en/stable/spreadsheet.html
    custom_request(request, fields, **kwargs)

    """
