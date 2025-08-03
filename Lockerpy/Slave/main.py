import network
import espnow 
import machine as mc
import time

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
key = b"pSW51#zEa7Tk6XrQ"
e.add_peer(mac[0], lmk=key)
#LED
def lightwait():
   led.value(True)
   time.sleep(0.5)
   led.value(False)
   time.sleep(0.5)
def loadc():
    try:
        with open("counter.txt") as f:
            return int(f.read())  # o int()
    except:
        return 2  # valor inicial
def savec(c):
 try:
  with open("counter.txt", "w") as f:
   f.write(str(c))
 except Exception as e:
  print("Error guardando contador:", e)

c = loadc()
last_c = c 

while True:
 host, msg = e.recv() # msg == None if timeout in recv()
 
 if msg:
  
  if host not in mac:
   print("wrong")
   lightwait()
   continue
   
  try:
   cmd, token, c = msg.decode().split(":") # split the code in three parts: (host, msg) msg = cmd and tkn  
   c = int (c)
   print("Comando:", cmd)
   print("Token recibido")

   if token != tkn:
     print("Not today, bud!")
     continue
   if c <= last_c:
    print("Error")
    continue
    
   last_c = c
   
   savec(last_c)

   if cmd == "RlQmXpne02MC6}Fdnt#8=SD?G,Xi":
    rele.value(True)
    led.value(True)
    print(f"Veces {last_c}")

   elif cmd == ";E7_+xtQpj83+!@x~1Nh>[4vzu65":
    rele.value(False)
    led.value(False)         
       
  except ValueError:
   print("Incorrect")
   continue