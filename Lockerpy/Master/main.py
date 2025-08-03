import network
import espnow 
import machine as mc
from DIYables_MicroPython_LCD_I2C import LCD_I2C
import time

pressedbutton = 0 
ulcmnd = None 
maximummodes = 2
lastpressedbutton = None
lcdstate = None
llastpressedbutton = None
Open = "RlQmXpne02MC6}Fdnt#8=SD?G,Xi"
Close = ";E7_+xtQpj83+!@x~1Nh>[4vzu65"
key = b"pSW51#zEa7Tk6XrQ"
I2C_ADDR = 0x27 
LCD_ROWS = 2 
LCD_COLS = 16
ledopa = mc.Pin(14, mc.Pin.OUT)
ledcla = mc.Pin(12, mc.Pin.OUT)
button = mc.Pin(4, mc.Pin.IN)
button1 = mc.Pin(16, mc.Pin.IN)
#Signals of activation:
led = mc.Pin(2, mc.Pin.OUT)
i2c = mc.I2C(1, scl=mc.Pin(22), sda=mc.Pin(21), freq=400000)
lcd = LCD_I2C(i2c, I2C_ADDR, LCD_ROWS, LCD_COLS)
lcd.backlight_on()
lcd.clear()
#activating connection ESPNOW
sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True) 
sta.disconnect() 
led.value(False)
e = espnow.ESPNow()
e.active(True)
peer = b"\x88\x13\xbf\x82\x37\x88" 
e.add_peer(peer, lmk = key) 
lcd.clear()
#tokens for different modes:
tokenmodebed = "LIEsw6qMzx99OHWKOmdhQXVMxS213Xt8R4cJnw3RYRmQyVqvo2" 
tokenmodelab = "J6pGUJscy1ZOdKuuFbXrRJtWBV916im8MhRhf3GY5TDmtFuWkfBPg6Gy" 
tokens = (tokenmodebed, tokenmodelab) #tokenlab, tokenbed
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
def activation(): # def for the activation
 if button.value() == True: 
  return Open #Open
 else:
  return Close #Closed
class LockerOutputs: #sends tokens
 def __init__(self,token): 
  self.token = token
class LCDMessage: #makes shorter the code since I do not have to write those 3 lines
 def __init__(self,lcdmsg):
  self.lcdmsg = lcdmsg
  lcd.clear()
  lcd.set_cursor(0,0)
  lcd.print(self.lcdmsg)
c = loadc()
while True:
 mensaje = activation() # the def is equal to mensaje
 if button1.value(): 
  pressedbutton += 1
  time.sleep(0.5)
 if pressedbutton == 0:
  token1 = LockerOutputs(tokens[0]) 
 elif pressedbutton == 1:
  token1 = LockerOutputs(tokens[1])
 if pressedbutton > maximummodes - 1: 
  pressedbutton = 0
  print("Reboot")
 try:  
  if mensaje != ulcmnd: # Sends 1 message to the receptor:
   msg = f"{mensaje}:{token1.token}:{c}".encode()
   print(token1.token)
   e.send(peer, msg) # Sends the message:
   print(f"Veces {c}")
   print(f"Enviado: {mensaje}")
   if mensaje == Open:
    LCDMessage("Opened")
    ledopa.value(True)
    ledcla.value(False)
   else:
    LCDMessage("Closed")
    ledopa.value(False)
    ledcla.value(True)
   c = int(c + 3)
   savec(c)
 except:
  print("Trying again")
  continue
 ulcmnd = mensaje