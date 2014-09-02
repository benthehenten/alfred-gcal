import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from pyrfc3339 import parse
from datetime import datetime
import pytz

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Developers Console
FLOW = OAuth2WebServerFlow(
    client_id='138764037090-uu3qk39ca5hbdknvlbkdt80erplg624r.apps.googleusercontent.com',
    client_secret='zChfyIDzXLoW3iIQbNQpWqtC',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='Alfred Gcal/0.1')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google Developers Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='138764037090')


#add the event
created_event = service.events().quickAdd(
    calendarId='primary',
    text='{query}').execute()

date = created_event["start"]["dateTime"]
# print date

# if(int(date[20:21]) > 11):
#     newHour = int(date[20:21]) - 12
#     niceTime = newHour + date[22:] + "pm"
# else:
#     niceTime = str(date[20:]) + "am"

# nicedate = date[5:10] + "-" + date[0:4] + " at " + niceTime

nicedate = parse(date).strftime("%B %d, %Y")

print created_event['summary'] + " on " + nicedate + " at " + created_event.get("location", "")




