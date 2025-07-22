import network
import espnow 
import machine as mc
import time

#variables
ulcmnd = None
button = mc.Pin(4, mc.Pin.IN)
led = mc.Pin(2, mc.Pin.OUT)

sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True) # A WLAN interface must be active to send()/recv()
sta.disconnect() # Because ESP8266 auto-connects to last Access Point
led.value(False)

e = espnow.ESPNow()
e.active(True)

peer = b"\x88\x13\xbf\x82\x37\x88" # identifier of the other ESP, the one esp we will connect
e.add_peer(peer)      # Must add_peer() before send()

token ="LIEsw6qMzx99OHWKOmdhQXVMxS213Xt8R4cJnw3RYRmQyVqvo2" 

while True:
 
 if button.value() == True: 
    mensaje = "Open"
 
 else:
    mensaje = "Close"
 
 if mensaje != ulcmnd:
   msg = f"{mensaje}:{token}".encode()
   e.send(peer, msg)
   print(f"Enviado: {mensaje}")
 
 ulcmnd = mensaje
