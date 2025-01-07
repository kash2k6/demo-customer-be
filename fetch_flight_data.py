from flask import Flask, request, jsonify
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/fetch-flight-data', methods=['GET'])
def fetch_flight_data():
    acid = request.args.get('acid')
    outdate = request.args.get('outdate')
    indate = request.args.get('indate')
    username = "trAPI"
    password = "EP5lGF8r5W"
    url = "https://xml.flightview.com/FlightStatusJsonDemo/fvxml.exe"

    params = {
        "acid": acid,
        "outdate": outdate,
        "indate": indate,
        "A": username,
        "B": password
    }

    response = requests.get(url, params=params)
    response_dict = response.json()

    flights = response_dict.get("Flights", [])
    flight_data_list = []
    for flight in flights:
        flight_data = {
            "FlightNumber": flight["Acid"]["FlightNumber"],
            "AirlineCode": flight["Acid"]["Airline"]["Code"],
            "DepartureAirportCode": flight["DepartureAirport"]["Code"],
            "ArrivalAirportCode": flight["ArrivalAirport"]["Code"],
            "ScheduledDeparture": flight["ScheduledDeparture"]["Local"],
            "ScheduledArrival": flight["ScheduledArrival"]["Local"],
            "Status": flight["Status"],
            "ServiceType": flight["ServiceType"],
            "DepartureTerminal": flight["DepartureTerminal"],
            "ArrivalTerminal": flight["ArrivalTerminal"],
        }
        flight_data_list.append(flight_data)

    datetime_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    document_name = f"flight_info_v2_req_{datetime_str}"

    doc_ref = db.collection('flightViewCalls').document(document_name)
    doc_ref.set({"flights": flight_data_list})

    return {"flights": flight_data_list}

@app.route('/duffel-flights-create-orders', methods=['POST'])
def create_duffel_flight_order():
    url = "https://api.duffel.com/air/orders"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v1",
        "Authorization": f"Bearer {os.getenv('DUFFEL_ACCESS_TOKEN')}"
    }
    data = request.json

    response = requests.post(url, headers=headers, json=data)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)