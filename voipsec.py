import os
from datetime import datetime
from twilio.rest import Client

account_sid = '-'
auth_token = '-'
twilio_number = '+14346942415'
client = Client(account_sid, auth_token)

calls = client.calls.list(
    to=twilio_number,
    start_time_after=datetime(2023, 4 ,6 , 0, 0, 0)
)

for c in calls:
    for r in c.recordings.list():
        message = client.recordings(r.sid).fetch()
        for t in message.transcriptions.list():
            print(c.sid, t.transcription_text)
            print()