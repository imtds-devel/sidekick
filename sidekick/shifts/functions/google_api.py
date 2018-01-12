import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'


def get_refresh_token():
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)

    storage = Storage("store-oauth2.json")
    args = tools.argparser.parse_args([])
    args.noauth_local_webserver = True
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, args)

    return credentials.refresh_token


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    flags = tools.argparser.parse_args([])

    credential_dir = "/var/www/html/.credentials"
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def build_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http)


