from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import json
import requests
import time
import asyncio
from aiocoap import *
import aiohttp
from coapthon.client.helperclient import HelperClient

app = Flask(__name__)

#--------------------Inizio Prova publish
def publish_message(topic, message):
    #client = mqtt.Client()
    #client.connect('mqtt', 1884, 60)  # Aggiungi l'indirizzo IP o il nome del broker MQTT e la porta corretti
    #client.publish(topic, message)
    return 'messaggio pubblicato'
#---------------------Fine Prova publish

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    json_payload = json.loads(payload)
    room = client.room
    json_payload['room'] = room
    # Richiesta POST    
    destination_url = 'http://flask-FirebaseWriter:5002/mqtt'
    # Costruisci l'header con il content type
    headers = {'Content-Type': 'application/json'}
    # Invia il payload come parte della richiesta POST
    response = requests.post(destination_url, headers=headers, json=json_payload)

    if response.status_code == 200:
        print("Richiesta POST inviata con successo.")
    else:
        print("Errore durante l'invio della richiesta POST.")
    

# Funzione per effettuare la subscribe al broker MQTT
def subscribe_to_mqtt_broker(broker_url, port, topics, room):
    client = mqtt.Client()
    client.brokerURL = broker_url
    client.room = room
    # Registra la funzione di callback
    client.on_message = on_message
    # Connessione al broker MQTT 
    client.connect(broker_url, port, keepalive=60)
    for topic in topics:
        client.subscribe(topic)
    #client.publish(topic, '{"glycemia":10000}')
    # Avvio del loop per mantenere la connessione MQTT
    client.loop_start()

def connect_to_http_url(destination_URL, room):
    print('entrato nella funzione connect http url')
    # Connessione all'URL ricevuto
    while True:
        response = requests.get(destination_URL)
        if response.status_code == 200:
            # Elabora la risposta e scarico il payload
            payload = response.json()  
            payload['room'] = room
            json_payload = json.dumps(payload)
            requests.post('http://flask-FirebaseWriter:5002/http', headers = {'Content-Type': 'application/json'}, data=json_payload)
            print('oggetto mandato al writer')
        else:
            # Gestisci eventuali errori di connessione
            print('Errore durante la richiesta GET:', response.status_code)
        
        time.sleep(10)

def connect_to_coap_url(server_url, port, path, room):
    print('Entrato nella funzione coap')
    # Connessione all'URL ricevuto
    server_ip = server_url
    #server_ip = '172.22.0.6'
    server_port = port
    path = '/' + path
    print(server_ip + ':' + str(server_port) + path) 
    # Crea un oggetto HelperClient per comunicare con il server CoAP
    client = HelperClient(server=(server_ip, server_port))

    while True:
    # Effettua una richiesta GET al percorso desiderato
        response = client.observe(path=path, callback=None)
        response_payload = response.payload
        new_string = response_payload.replace("\\", "").strip("\"")
        new_string_json = json.loads(new_string)
        new_string_json["room"] = room
        print(new_string_json)
        json_payload = json.dumps(new_string_json)
        requests.post('http://flask-FirebaseWriter:5002/coap', headers = {'Content-Type': 'application/json'}, data=json_payload)
        print('Correttamente mandato al server')

        time.sleep(5)


        
# Endpoint per la richiesta POST
@app.route('/mqtt', methods=['POST'])
def handle_mqtt_request():
    payload = request.get_json()
        
    # Eseguire la subscribe al broker MQTT
    broker_url = payload.get('brokerURL')  # Imposta il valore di "brokerURL" ottenuto dalla richiesta POST
    room = payload.get('room')
    port = payload.get('port')
    topics = payload.get('topics')
    subscribe_to_mqtt_broker(broker_url, port, topics, room)

    # Costruisci il payload della risposta
    response_data = {
        'brokerURL': broker_url,
        'port': port,
        'room': room,
        'topics': topics,
        'message': 'Richiesta POST ricevuta correttamente'
    }

    # Restituisci una risposta JSON
    return jsonify(response_data)

@app.route('/http', methods=['POST'])
def handle_http_request():
    print('entrato nell\'endpoint http')
    payload = request.get_json()  # Ottieni il payload dalla richiesta POST come JSON
    print(payload)

    #-----CONTROLLI DA AGGIUNGERE
    #if 'url' not in payload:
    #    return 'URL mancante nel payload', 400

    server_url = payload.get('serverURL')
    port = payload.get('port')
    path = payload.get('path')
    room = payload.get('room')

    destination_URL = f"http://{server_url}:{port}/{path}"
    print(destination_URL)
    connect_to_http_url(destination_URL, room)

    return 'Funzione make_get_request'

@app.route('/coap', methods=['POST'])
def handle_coap_request():
    print('entrato nell\'endpoint coap')
    payload = request.get_json()  # Ottieni il payload dalla richiesta POST come JSON
    print(payload)

    server_url = payload.get('serverURL')
    port = payload.get('port')
    path = payload.get('path')
    room = payload.get('room')

    connect_to_coap_url(server_url, port, path, room)

    return 'Funzione handle_coap_request'
    
@app.route('/')
def hello_app1():
        
    return 'Hello from app1-microservice1!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
