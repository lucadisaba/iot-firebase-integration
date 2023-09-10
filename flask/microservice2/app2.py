from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import json


# Inizializza l'applicazione Firebase
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "bindingmqttfirebase",
  "private_key_id": "358aa690a93e1c712d4f11a974e3706cab9d92f9",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQC0/EqwK+XaMuNX\nczBqpb6w6YtNlW4bC4WTQDMDlcX0jWddOOE7sdkBapd0o/phgc7WdG1wYDZnn1ge\nvFZ3ZcsPO3N6IU5Ey3983VYvEWSdq3h2O8xKMAgNG6Ak4ntqP9P+Ok5QSQvUnMlU\n19MQh9J7tq2CpjkJBYRERKqwpiG6Nuo7t0s8c8sLik1ecApciES5ogaK1AsQlAhL\n6c2woNJfdm5Yf2v16NOZ4r9yiF0TGu484rRrWghluBQniV1TEzrWlt0PPdwIcDgR\nrs552zMUYeqkRbzMHWFbr6f4qiW3yKq8mrUlrQ3jveusA7S+OtSC6G7qUcuCXQTZ\n/zIeq9HFAgMBAAECgf8mR43PdsqdgYON9Uv9W43/6aQWedwIJ0h9OkKisW7iMcGe\ni9/r+IYfe6RCMxtw7lscE5CIyg80o2AMfdXMAQBoj8aYM8RaMslzCah1kMfQLYcO\nmhQelp/+GUPe7TP1ExqX1p3+diONj/ND2TaMuOjeuGb0TfWc06bbLYVpmQr/zhwW\nWThiivpxIg53OKy43PoRAl+/ahirZ8Z6a4y6gKbSTg102wezLwSg2yHIWXIRuSly\nDPR1tP+l9myxkF0ZlsVoRiUZSNY4/sooYQv4YEhC1tyxMwOS8+Glyht1YXrE541O\nrCeQNb//iVkOu1I2RloY3wFs/sM4c4lYhOTLqBECgYEA+jyZrRnU+vMFv8mxoHJp\nqSQQRaFY0DSgDpxFGYLC+kUmnw7q+TUz5Aj8M2Cwa/spfLjx6pp5YYDin/eJSnYC\nvOjUpLGixy7Nlg7LITQxwChqvvgjjtT3tw4kZcT+ivu1GLTNDMtg5efHt7lt7PLj\nTI2fXm26aaUWVKnPavS87EcCgYEAuSdinwytWuRUiBkUlRQ0GJKjC0lFTsHw8xZF\nyFk1aoUvFDiZ/UWxT3mCqgfXcH+BTVDGEtGrK1Nft+N8OmQ1FG7QVHhJ+TLCv2Kc\nQJul8uhG9ok/tLAKQfzDxNWv7uXZjC+QUTZw2B/anutKMDCnbjbEiu6E9sEqbn7M\noKjyM5MCgYBxPOUqIStxGHJ8lLAt9Dh+UxSN/fKr3XSkx/C5F6RWDt7oUZ7hgULn\nKW2/bjzH0JO4nhTTXm4ZQnLLgv/80yRwCkjX8o6/5h0gj7c6Yl01INUVcELfCt7C\nVsL/zsKFcFxGPuMfrBVAVL/bEy18cXmMlfYNjEg0MIHHdESpmPC5VwKBgFgEAvu8\nmQPmGtD/qysbCZDM1DjfQdUomJPV+KI+1gem/DROm9UsNhejmZueUqml0x+f0CjO\nBuJ3pb7SoxFW5WyrKNmevPt7R9yW0dRcqUyJYoJ7yA7qyFWKBL4jHpkgJoRfb+lL\nSeVTbyewjfnOhyj7W/73V7m9JaCVIk0VQt2FAoGAHGD0jX9oswkKaUG7UB29B/Gz\nhhZfwp8y7nA9/opZzQ0odkTP/7qGwVmjWV4R19i/eE4I7uopfkOrjO4KlXioqmgW\npU4OUEV7emMfx2x0XJbOBpEGunoPgNW45oeRD5tG7400NdErUmIfXW0fl8hosbhe\n+ka6ym4kZ+3T4Q9xLQM=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-rh70z@bindingmqttfirebase.iam.gserviceaccount.com",
  "client_id": "112726474938409098275",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-rh70z%40bindingmqttfirebase.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route('/mqtt', methods=['POST'])
def on_message_mqtt():
    # Inserisci il payload nel database Firebase Firestore
    payload = request.get_json()
    # Accedo al rispettivo sensore
    room = payload.get('room')
    topic = payload.get('topic')
    sensor_value = payload.get('sensor_value')
    
    #id_sensor = str(uuid.uuid4())
    # Crea un documento nel tuo database 
    doc_ref = db.collection('sensors').document(room)
    doc_ref.set({
        'IoT_data': {
            topic: sensor_value
        }
    }, merge=True)

    return 'Payload inserito correttamente nel database Firestore'

@app.route('/http', methods=['POST'])
def on_message_http():
    # Inserisci il payload nel database Firebase Firestore
    payload = request.get_json()
    print(payload)
    # Accedo al rispettivo sensore
    room = payload.get('room')
    url = payload.get('url')
    sensor_value = payload.get('sensor_value')
    
    # Crea un documento nel tuo database 
    doc_ref = db.collection('sensors').document(room)
    doc_ref.set({
        'IoT_data': {
            url: sensor_value
        }
    }, merge=True)

    return 'Payload inserito correttamente nel database Firestore'

@app.route('/coap', methods=['POST'])
def on_message_coap():
    # Inserisci il payload nel database Firebase Firestore
    payload = request.get_json()
    print(payload)
    # Accedo al rispettivo sensore
    room = payload.get('room')
    url = payload.get('url')
    sensor_value = payload.get('sensor_value')
    
    #id_sensor = str(uuid.uuid4())
    # Crea un documento nel tuo database 
    doc_ref = db.collection('sensors').document(room)
    doc_ref.set({
        'IoT_data': {
            url: sensor_value
        }
    }, merge=True)

    return 'Payload inserito correttamente nel database Firestore'
    

@app.route('/')
def hello_app2():
    return 'Hello from app2-microservice2!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
