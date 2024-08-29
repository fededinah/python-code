import asyncio
import websockets
import json
import sys
from datetime import datetime, timezone

async def connect_ais_stream():

    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "e9c5708566c74820c7b625c395e2edadb340d994", 
                             "BoundingBoxes": [[[9, 49], [59, -30]]]}

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)
        
        


        #scelgo quanti oggetti salvare (per ogni tipo)
        bound = 30000

        #definisco i contatori per implementare l'arresto ed inizializzo le liste di oggetti
        countStatic = 0
        countPosition = 0
        staticData = []
        positionData = []

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]
            if message_type == "ShipStaticData" and countStatic < bound:
                #ais_message = message['Message']['ShipStaticData']
                #print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Longitude: {ais_message['Longitude']}")
                
                '''
                An ShipStaticData AIS message contains static data about the vessel, such as its name, call sign, length, 
                width, and type of vessel. It also includes information about the vessel's owner or operator, as well as 
                its place of build and its gross tonnage. This message is transmitted at regular intervals, usually every 
                few minutes, and is used by other vessels and coastal authorities to identify and track the vessel. It is 
                an important safety feature that helps to prevent collisions and improve navigation in crowded waterways.

                '''
                #normalizzo i dati
                message['Message']['ShipStaticData']['Destination'] = message['Message']['ShipStaticData']['Destination'].strip()
                message['Message']['ShipStaticData']['Name'] = message['Message']['ShipStaticData']['Name'].strip()
                message['Message']['ShipStaticData']['CallSign'] = message['Message']['ShipStaticData']['CallSign'].strip()
                message['MetaData']['ShipName'] = message['MetaData']['ShipName'].strip()
                
                #appendo l'oggetto appena letto alla relativa lista e aggiorno il contatore
                staticData.append(message)
                countStatic += 1

            elif message_type == "PositionReport" and countPosition < bound:

                '''
                An PositionReport AIS message is used to report the vessel's current position, heading, speed, and other 
                relevant information to other vessels and coastal authorities. This message includes the vessel's unique 
                MMSI (Maritime Mobile Service Identity) number, the latitude and longitude of its current position, the 
                vessel's course over ground (COG) and speed over ground (SOG), the type of navigation status the vessel is 
                in (e.g. underway using engine, anchored, etc.), and the vessel's dimensional information (length, width, 
                and type). This information is used to help identify and track vessels in order to improve safety, efficiency,
                and compliance in the maritime industry.
                
                '''
                #normalizzo i dati
                message['MetaData']['ShipName'] = message['MetaData']['ShipName'].strip()
                
                #appendo l'oggetto appena letto alla relativa lista e aggiorno il contatore
                positionData.append(message)
                countPosition += 1

            #implementazione dell'arresto
            if countStatic == bound and countPosition == bound:
            
                #creo il dizionario composto dalle liste aggiornate con i nuovi dati estratte
                dataDict = {'n_elem':  bound, 'ShipStaticData': staticData, 'PositionReport': positionData}
                #salvo i dati nel file json
                with open('dataShip_ww_new_daily.json', 'w') as file:
                    json.dump(dataDict, file, indent=4)
                sys.exit(f"{bound} elementi elaborati")

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())



