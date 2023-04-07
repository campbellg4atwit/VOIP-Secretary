import os
from datetime import datetime
from twilio.rest import Client

account_sid = 'AC909cf9f7b41e1ef51e3fab1e8f140202'
auth_token = '90e9aaa2b9e42acd1d1aa4c53837a370'
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