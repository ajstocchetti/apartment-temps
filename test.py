import time
import board
import adafruit_dht
from influxdb import InfluxDBClient

 
# Initial the dht device, with data pin connected to:
DHT_TYPE = adafruit_dht.DHT22
DHT_PIN  = board.D4
dhtDevice = DHT_TYPE(DHT_PIN)

minF = 65
lowFreq = 30 # seconds
regFreq = 240 # seconds
errorFreq = 6 # seconds

client = InfluxDBClient(host='127.0.0.1', port=8086, database='apartmenttemp')

def getFrequency(tempReading, isValid):
    if isValid is not True:
        return errorFreq
    elif tempReading > minF:
        return regFreq
    else:
        return lowFreq

def getVals():
    resp = {
        "temp": None,
        "humidity": None
    }
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        temperature_f = round(temperature_f, 3)
        resp["temp"] = temperature_f
        humidity = dhtDevice.humidity
        resp["humidity"] = humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    finally:
        return resp

def handleResp(vals, isValid):
    try:
        if isValid:
            insertTsdb(vals)
        print("Temp: {:.1f} F - Humidity: {}% "
            .format(vals.get("temp"), vals.get("humidity")))
    except:
        pass


def run():
    vals = getVals()
    temp = vals.get("temp")
    isValidRead = temp is not None
    handleResp(vals, isValidRead)
    nextFreq = getFrequency(temp, isValidRead)
    print("Sleeping for", nextFreq, "seconds")
    time.sleep(nextFreq)


def insertTsdb(vals):
    body = [
        {
            "measurement": "climate",
            "tags": {
                "location": "bedroom",
                "device": "pi3b"
            },
            "fields": vals
        }
    ]
    client.write_points(body)


while True:
    run()
