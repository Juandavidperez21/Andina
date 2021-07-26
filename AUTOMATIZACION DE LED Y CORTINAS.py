from machine import Pin, PWM, ADC, 
import utime
import network, time, urequests
from machine import Pin
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import framebuf

ancho = 128
alto = 64

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)

def buscar_icono(ruta):
    dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

oled.blit(buscar_icono("dibujo/dibujoled.pbm"), 0, 0) # ruta y sitio de ubicación
oled.show()  #mostrar
time.sleep(2)


def conectaWifi(red, password):
     global miRed
     miRed = network.WLAN(network.STA_IF)     
     if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect('FAMILIAPYL', 'SJEAMGET88*')         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
     return True
    
sensor = ADC(Pin(36))

if conectaWifi("FAMILIAPYL", "SJEAMGET88*"):

    print("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
 
def main():
    
    sensor = ADC(Pin(36))
    sensor.width(ADC.WIDTH_10BIT)  # permite regular la precisión de lectura
    sensor.atten(ADC.ATTN_11DB) 
    servo = PWM(Pin(14), freq = 0)
    led = PWM(Pin(13), freq = 285) 
    
    
    def map(x):
        return int((x - 0) * (130- 34) / (180 - 0) + 34)
    
    def map_adc(x):
        return int((x - 0) * (1023- 0) / (130 - 34) + 0)
    
    url = "https://maker.ifttt.com/trigger/movimiento_en_casa/with/key/cMJmjYmQZWSvR53nGZFCr6?"
    
    while True:
                   
        lectura =  float(sensor.read())
        print(lectura)
        angulo = map_adc(lectura)              
        m = map(angulo)
        servo.duty(m)
        led.duty(m)
        utime.sleep(0)  
        print(m)
        
        sensor.read()
        motor=sensor.read()
        
        
        if motor > 1000 :
            respuesta = urequests.get(url)      
            print(respuesta.text)
            print (respuesta.status_code)
            respuesta.close ()
            
        if motor < 100 :
            respuesta = urequests.get(url)      
            print(respuesta.text)
            print (respuesta.status_code)
            respuesta.close ()
                  
            
if __name__ == '__main__':
    main()+