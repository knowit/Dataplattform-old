from __future__ import print_function
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from airtable import Airtable


# Airtable API settings
airtable_api_key = ""
airtable_base_id = ""
airtable_table_name = ""

# Goggle sheet API settings
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ""
SAMPLE_RANGE_NAME = ""

# CVPartner API settings
cvpartner_api_key = ""

# Columns
EMAIL = 1
NAME = 2
TITLE = 3
ABSTRACT = 4
SPEAKER_DESCRIPTION = 5
IMAGE_URL = 6
SPARE_TIME = 7
FAV_FOOD = 8
FAV_MUSIC = 9
FAV_TRAVEL = 10
FAV_TV_MOV = 11
FAV_PLACE = 12
CONSENT = 13
USE_CVPARTNER_IMAGE = 14


def main():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result['values']

    # Init airtable
    airtable = Airtable(airtable_base_id, airtable_table_name, api_key=airtable_api_key)

    if not values:
        print('No data found.')
    else:
        for row in values:
            update_airtable(airtable, row)


def update_airtable(airtable, row):
    """
    Searches for a corresponding record in airtable based on email,
    name and talk title from google sheet and updates the record
    """

    sheet_data, use_cvpartner_image = parse_row(row)

    # search first on email
    record = airtable.search('email', sheet_data['email'])

    if not record:
        # search for name
        record = airtable.search('userIds', sheet_data['userIds'])

        # lastly search for talk title
        if not record:
            record = airtable.search('title', sheet_data['title'])

    if record:
        # special case
        # if a person has two talks, do not update anything
        if len(record) > 1:
            return

        if use_cvpartner_image:
            image_url = get_cvpartner_image_url(sheet_data['email'])
            if image_url:
                filename = sheet_data['email'].split('@', 1)[0]
                image_object = make_attachment_obj(image_url, filename)
                sheet_data['speaker_image'] = image_object

        record_id = record[0]['id']
        airtable.update(record_id, sheet_data)


def parse_row(row):
    """ Parses data from the google sheet
    """
    sheet_data = {}
    use_cvpartner_image = False


    while len(row) < 16:
        row.append('')

    sheet_data['email'] = row[EMAIL]
    if row[NAME]:
        sheet_data['userIds'] = row[NAME]
    if row[TITLE]:
        sheet_data['title'] = row[TITLE]
    if row[ABSTRACT]:
        sheet_data['description'] = row[ABSTRACT]
    if row[SPEAKER_DESCRIPTION]:
        sheet_data['speaker_bio'] = row[SPEAKER_DESCRIPTION]
    if row[IMAGE_URL]:
        sheet_data['speaker_image_url'] = row[IMAGE_URL]
    if row[SPARE_TIME]:
        sheet_data['speaker_recreation'] = row[SPARE_TIME]
    sheet_data['speaker_favourites'] = row[FAV_FOOD]+';'+row[FAV_MUSIC]+';'+row[FAV_TRAVEL]+';'\
                                       +row[FAV_TV_MOV]+';'+row[FAV_PLACE]

    if row[CONSENT]:
        sheet_data['speaker_consent'] = True
    else:
        sheet_data['speaker_consent'] = False

    if row[USE_CVPARTNER_IMAGE]=='Ja, jeg ønsker at dere bruker bildet fra CVPartner':
        use_cvpartner_image = True

    return sheet_data, use_cvpartner_image


def get_cvpartner_image_url(email):
    """ Fetches url for image on cvpartner
        Returns None if not found
    """

    url = f"https://knowit.cvpartner.com/api/v1/users/find?email={email}"
    headers = {'Authorization': 'Token token={}'.format(cvpartner_api_key)}
    try:
        response = requests.get(url, headers=headers).json()

        user_id = response["user_id"]
        default_cv_id = response["default_cv_id"]

        url = f"https://knowit.cvpartner.com/api/v3/cvs/{user_id}/{default_cv_id}"
        response = requests.get(url, headers=headers).json()

        image_url = response["image"]["url"]
        return image_url

    except:
        print("No data on "+email+" found at knowit.cvpartner.com")

    return None

def make_attachment_obj(image_url, filename):
    """
    Creates an attachement object  for an
    airtable attachment column type
    """

    image_object =\
        [
            {
                "url": image_url,
                "filename": filename,
            }
        ]
    return image_object


if __name__ == '__main__':
    main()


