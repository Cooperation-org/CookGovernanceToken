import os
import pygsheets

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
