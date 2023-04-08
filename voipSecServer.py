from flask import Flask
from flask import render_template
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.rest import Client 
 
account_sid = 'AC909cf9f7b41e1ef51e3fab1e8f140202' 
auth_token = '' 
client = Client(account_sid, auth_token) 
twilio_number = '+14346942415'

app = Flask(__name__)

@app.route("/msg", methods=['GET', 'POST'])
def msg():
    sender = request.form['From']
    #session_id = request.values['SessionID']
    message_body = request.form['Body']

    calls = client.calls.list(limit=20)

    if "transcription" in message_body:
        for c in calls:
            for r in c.recordings.list():
                message = client.recordings(r.sid).fetch()
                for t in message.transcriptions.list():
                    message = client.messages.create(
                                body="[From:" + c.from_formatted + "] " + t.transcription_text,
                                from_=twilio_number,
                                to=sender
                            )

    
    return str()

if __name__ == "__main__":
    app.run(debug=True, port=5025, host="0.0.0.0")
