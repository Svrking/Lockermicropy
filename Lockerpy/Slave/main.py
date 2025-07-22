import network
import espnow 
import machine as mc
import time

#ESPNOW conection

sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True) # A WLAN interface must be active to send()/recv()
sta.disconnect() # Because ESP8266 auto-connects to last Access Point
e = espnow.ESPNow()
e.active(True)

#variables

rele = mc.Pin(4, mc.Pin.OUT)
led = mc.Pin(2, mc.Pin.OUT) 

#security

tkn = "LIEsw6qMzx99OHWKOmdhQXVMxS213Xt8R4cJnw3RYRmQyVqvo2" #token
mac = [b"\x88\x13\xbf\x82*\xe0"] #88:13:bf:82:2a:e0 normal mac

#LED

def lightwait():
   led.value(True)
   time.sleep(0.5)
   led.value(False)
   time.sleep(0.5)

while True:
 host, msg = e.recv() # msg == None if timeout in recv()
 
 if msg:
  
  if host not in mac:
   print("wrong")
   lightwait()
   continue
   
  try:
        cmd, token = msg.decode().split(":") # split the code in three parts: (host, msg) msg = cmd and tkn  
        print("Comando:", cmd)
        print("Token recibido")
        
        if token != tkn:
         print("Not today, bud!")
         continue
        
        else: 
         if cmd == "Open":
           rele.value(True)
           led.value(True)
         elif cmd == "Close":
           rele.value(False)
           led.value(False)         
       
  except ValueError:
        print("Incorrect")
