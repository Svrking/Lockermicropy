import network
import espnow 
import machine as mc
import time
#Buttons modes:
pressedbutton = 0 
ulcmnd = None 
maximummodes = 2 # the quantity of modes that the locker supports
lastpressedbutton = None
#Buttons values:
button = mc.Pin(4, mc.Pin.IN)
button1 = mc.Pin(16, mc.Pin.IN)
#Signals of activation:
led = mc.Pin(2, mc.Pin.OUT)
#activating connection ESPNOW
sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True) # A WLAN interface must be active to send()/recv()
sta.disconnect() # Because ESP8266 auto-connects to last Access Point
led.value(False)
e = espnow.ESPNow()
e.active(True)
peer = b"\x88\x13\xbf\x82\x37\x88" # identifier of the other ESP, the one esp we will connect
e.add_peer(peer) # Must add_peer() before send()
#tokens for different modes:
tokenmodebed = "LIEsw6qMzx99OHWKOmdhQXVMxS213Xt8R4cJnw3RYRmQyVqvo2" #
tokenmodelab = "J6pGUJscy1ZOdKuuFbXrRJtWBV916im8MhRhf3GY5TDmtFuWkfBPg6Gy" #
tokens = (tokenmodebed, tokenmodelab) #tokenlab, tokenbed

def activation(): # def for the activation

 if button.value() == True: 
  return "Open"
  
 else:
  return "Close"

class LockerOutputs:
  
 def __init__(self,token): # 
  self.token = token
 
while True:
 mensaje = activation() # the def is equal to mensaje
 if button1.value(): 
  pressedbutton +=1
  time.sleep(0.5)
 
 if pressedbutton == 0:
  token1 = LockerOutputs(tokens[0]) # Searchs on the tuple where the token is

 elif pressedbutton == 1:
  token1 = LockerOutputs(tokens[1])

 if pressedbutton > maximummodes - 1: 
  pressedbutton = 0
  print("Reboot")
 try: 
  if mensaje != ulcmnd: # Sends mesage 1 time to the receptor:
   msg = f"{mensaje}:{token1.token}".encode()
   print(token1.token)
   e.send(peer, msg) # Sends the message:
   print(f"Enviado: {mensaje}") 
 except:
  print("Trying again")
  continue
 ulcmnd = mensaje