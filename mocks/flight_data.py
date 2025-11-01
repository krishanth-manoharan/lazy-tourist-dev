"""Mock flight data for testing"""

# Mock flight data - Outbound flights
MOCK_FLIGHTS = {
    "NYC-PARIS": [
        {
            "airline": "Air France",
            "flight_number": "AF007",
            "departure": "JFK",
            "arrival": "CDG",
            "duration": "7h 30m",
            "price": 650,
            "stops": 0,
            "departure_time": "22:30",
            "arrival_time": "12:00+1"
        },
        {
            "airline": "Delta",
            "flight_number": "DL264",
            "departure": "JFK",
            "arrival": "CDG",
            "duration": "8h 15m",
            "price": 580,
            "stops": 0,
            "departure_time": "18:15",
            "arrival_time": "07:30+1"
        },
        {
            "airline": "United",
            "flight_number": "UA57",
            "departure": "EWR",
            "arrival": "CDG",
            "duration": "7h 45m",
            "price": 720,
            "stops": 0,
            "departure_time": "20:00",
            "arrival_time": "09:45+1"
        }
    ],
    "NYC-BALI": [
        {
            "airline": "Qatar Airways",
            "flight_number": "QR701",
            "departure": "JFK",
            "arrival": "DPS",
            "duration": "22h 30m",
            "price": 1150,
            "stops": 1,
            "layover": "DOH - 3h 20m",
            "departure_time": "23:00",
            "arrival_time": "06:30+2"
        },
        {
            "airline": "Singapore Airlines",
            "flight_number": "SQ21",
            "departure": "JFK",
            "arrival": "DPS",
            "duration": "24h 15m",
            "price": 1280,
            "stops": 1,
            "layover": "SIN - 4h 10m",
            "departure_time": "01:30",
            "arrival_time": "10:45+2"
        },
        {
            "airline": "Korean Air",
            "flight_number": "KE086",
            "departure": "JFK",
            "arrival": "DPS",
            "duration": "23h 45m",
            "price": 1050,
            "stops": 1,
            "layover": "ICN - 2h 50m",
            "departure_time": "13:45",
            "arrival_time": "22:30+2"
        }
    ],
    "NYC-TOKYO": [
        {
            "airline": "ANA",
            "flight_number": "NH9",
            "departure": "JFK",
            "arrival": "NRT",
            "duration": "14h 10m",
            "price": 950,
            "stops": 0,
            "departure_time": "13:10",
            "arrival_time": "16:20+1"
        },
        {
            "airline": "JAL",
            "flight_number": "JL006",
            "departure": "JFK",
            "arrival": "HND",
            "duration": "13h 50m",
            "price": 1020,
            "stops": 0,
            "departure_time": "11:50",
            "arrival_time": "14:40+1"
        }
    ],
    "DEFAULT": [
        {
            "airline": "International Airways",
            "flight_number": "IA123",
            "departure": "ORIGIN",
            "arrival": "DEST",
            "duration": "8h 00m",
            "price": 800,
            "stops": 0,
            "departure_time": "10:00",
            "arrival_time": "18:00"
        },
        {
            "airline": "Global Airlines",
            "flight_number": "GA456",
            "departure": "ORIGIN",
            "arrival": "DEST",
            "duration": "9h 30m",
            "price": 650,
            "stops": 1,
            "layover": "HUB - 2h",
            "departure_time": "14:00",
            "arrival_time": "23:30"
        }
    ]
}

# Mock return flight data
MOCK_RETURN_FLIGHTS = {
    "PARIS-NYC": [
        {
            "airline": "Air France",
            "flight_number": "AF008",
            "departure": "CDG",
            "arrival": "JFK",
            "duration": "8h 45m",
            "price": 680,
            "stops": 0,
            "departure_time": "14:30",
            "arrival_time": "17:15"
        },
        {
            "airline": "Delta",
            "flight_number": "DL265",
            "departure": "CDG",
            "arrival": "JFK",
            "duration": "9h 20m",
            "price": 610,
            "stops": 0,
            "departure_time": "11:00",
            "arrival_time": "13:20"
        },
        {
            "airline": "United",
            "flight_number": "UA58",
            "departure": "CDG",
            "arrival": "EWR",
            "duration": "8h 30m",
            "price": 750,
            "stops": 0,
            "departure_time": "16:45",
            "arrival_time": "19:15"
        }
    ],
    "BALI-NYC": [
        {
            "airline": "Qatar Airways",
            "flight_number": "QR702",
            "departure": "DPS",
            "arrival": "JFK",
            "duration": "23h 15m",
            "price": 1200,
            "stops": 1,
            "layover": "DOH - 3h 40m",
            "departure_time": "23:45",
            "arrival_time": "08:00+2"
        },
        {
            "airline": "Singapore Airlines",
            "flight_number": "SQ22",
            "departure": "DPS",
            "arrival": "JFK",
            "duration": "25h 00m",
            "price": 1320,
            "stops": 1,
            "layover": "SIN - 4h 30m",
            "departure_time": "02:15",
            "arrival_time": "12:15+2"
        },
        {
            "airline": "Korean Air",
            "flight_number": "KE087",
            "departure": "DPS",
            "arrival": "JFK",
            "duration": "24h 20m",
            "price": 1100,
            "stops": 1,
            "layover": "ICN - 3h 10m",
            "departure_time": "14:30",
            "arrival_time": "23:50+2"
        }
    ],
    "TOKYO-NYC": [
        {
            "airline": "ANA",
            "flight_number": "NH10",
            "departure": "NRT",
            "arrival": "JFK",
            "duration": "12h 50m",
            "price": 980,
            "stops": 0,
            "departure_time": "18:30",
            "arrival_time": "17:20"
        },
        {
            "airline": "JAL",
            "flight_number": "JL005",
            "departure": "HND",
            "arrival": "JFK",
            "duration": "12h 30m",
            "price": 1050,
            "stops": 0,
            "departure_time": "16:20",
            "arrival_time": "14:50"
        }
    ],
    "DEFAULT": [
        {
            "airline": "International Airways",
            "flight_number": "IA124",
            "departure": "DEST",
            "arrival": "ORIGIN",
            "duration": "8h 30m",
            "price": 820,
            "stops": 0,
            "departure_time": "11:00",
            "arrival_time": "19:30"
        },
        {
            "airline": "Global Airlines",
            "flight_number": "GA457",
            "departure": "DEST",
            "arrival": "ORIGIN",
            "duration": "10h 00m",
            "price": 680,
            "stops": 1,
            "layover": "HUB - 2h 30m",
            "departure_time": "15:30",
            "arrival_time": "01:30+1"
        }
    ]
}

