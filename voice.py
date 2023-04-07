from flask import Flask
from flask import render_template
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.rest import Client 
 
account_sid = '' 
auth_token = '' 
client = Client(account_sid, auth_token) 

app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a 'Hello world' message"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.play('https://wenge-chameleon-3671.twil.io/assets/clip.mp3')

    return str(resp)

@app.route("/clip")
def clip():
    return render_template('audio.html')

@app.route("/msg", methods=['GET', 'POST'])
def msg():
    number = request.form['From']
    #session_id = request.values['SessionID']
    session_id = 1
    print(number)
    message_body = request.form['Body']

    message = client.messages.create(  
                              messaging_service_sid='MG9afc5486825735b428dc1e7bfd8daf13', 
                              body='Creating conference',      
                              to=number 
                          ) 

    call = client.calls.create(
                        to=number,
                        from_=message_body,
                        url='https://listen.kshanley.xyz/joinConf/'+str(session_id),
                        status_callback_event=['completed'],
                        status_callback='https://listen.kshanley.xyz/completeCall/'+str(session_id)
                    )

    dial = Dial()
    dial.conference(session_id,     
        waitUrl='https://twimlets.com/holdmusic?Bucket=my-static-music',
        status_callback='https://listen.kshanley.xyz/leave',
        status_callback_event="leave join")
    
    return str()

@app.route('/joinConf/<string:call_session_id>', methods=['GET', 'POST'])
def conferenceCall(call_session_id):
   print("## Making a conference call")
   resp = VoiceResponse()
   dial = Dial()
   dial.conference(call_session_id,
                   waitUrl='',
                   status_callback='https://listen.kshanley.xyz/leave',
                   status_callback_event="leave")
   resp.append(dial)
   return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5025, host="0.0.0.0")
