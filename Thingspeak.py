#Envia temperatura y humedad a Thingspeak

import network, time, urequests
from dht import DHT11
from machine import Pin

def conectaWifi(red, password):
     global miRed
     miRed = network.WLAN(network.STA_IF)     
     if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect('FAMILIA PENA', 'Hupe6493$')         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
     return True


sensorDHT = DHT11 (Pin(15))

if conectaWifi("FAMILIA PENA", "Hupe6493$"):

    print("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
      
    url = "https://api.thingspeak.com/update?api_key=5ZQLSQT7L5MQAR68"  
    
    while (True):
        time.sleep (4)
        sensorDHT.measure()
        temp=sensorDHT.temperature()
        hum=sensorDHT.humidity()
        print ("T={:02d} ºC, H={:02d} %".format (temp,hum))

        respuesta = urequests.get(url+"&field1="+str(temp)+"&field2="+str(hum))
        print(respuesta.text)
        print (respuesta.status_code)
        respuesta.close ()
 
else:
       print ("Imposible conectar")
       miRed.active (False)