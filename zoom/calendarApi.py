import datetime
import sys
import auth


service = None

try:
    service = auth.getService()
except:
    print("error", sys.exc_info())
    exit()

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime',
                                    fields='items(description,end/dateTime,start/dateTime)').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = datetime.datetime.fromisoformat(event['start'].get('dateTime', 0))
    end = datetime.datetime.fromisoformat(event['end'].get('dateTime', 0))
    description = event["description"]
    format = "%w %H %M"
    print(f'{description} {start.strftime(format)} {end.strftime(format)}')
