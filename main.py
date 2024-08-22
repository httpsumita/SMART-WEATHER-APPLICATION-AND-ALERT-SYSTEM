import machine
import urequests 
from machine import Pin,ADC
import network, time
from dht import DHT11

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'CIXL0H98X94LP4TX'
adc=machine.ADC(26)
conversion_factor=100/65535
 
ssid = 'Redmi 11 Prime 5G'
password = 'pranoy@2004'
 
# Configure Pico W as Station
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)
 
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
     pass
print('network config:', sta_if.ifconfig()) 
 
while True:
    rainCoverage=100 -(adc.read_u16()*conversion_factor)
    time.sleep(5) 
    pin = Pin(10, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    t  = (sensor.temperature)
    h = (sensor.humidity)
    rainCoverage=round(rainCoverage,2)
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))
    print(round(rainCoverage,2),"%")
    print("Rain:{:.2f}%  "  .format(rainCoverage))
    dht_readings = {'field1':t, 'field2':h}
    rain_readings={'field3':rainCoverage}
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = dht_readings, headers = HTTP_HEADERS )  
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = rain_readings, headers = HTTP_HEADERS )  
    request.close() 
    print(dht_readings)
    print(rain_readings)
