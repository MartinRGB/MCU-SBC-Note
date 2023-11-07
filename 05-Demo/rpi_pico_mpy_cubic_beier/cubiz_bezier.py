# WS 320x240 display example
from machine import Pin,SPI,PWM,Timer
import framebuf
import utime
import os
import gc
import math
import random

def report():
    gc.enable()
    print("Allocated: " +str(gc.mem_alloc()))
    print("Free: "+str(gc.mem_free()))
    print("----------------")
    gc.collect()
    print("Allocated: " +str(gc.mem_alloc()))
    print("Free: "+str(gc.mem_free()))
    print("================\n")
    
print("Imports & Reporting")
report()

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD_1inch3(framebuf.FrameBuffer): # For 320x240 display
    def __init__(self):
        self.width = 320
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        self.BALCK =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3f)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        

# Colour Mixing Routine
def colour(R,G,B): # Compact method!
    mix1 = ((R&0xF8)*256) + ((G&0xFC)*8) + ((B&0xF8)>>3)
    return  (mix1 & 0xFF) *256  + int((mix1 & 0xFF00) /256) # low nibble first

def ring(cx,cy,r,cc):   # Draws a circle - with centre (x,y), radius, colour 
    for angle in range(91):  # 0 to 90 degrees in 2s
        y3=int(r*math.sin(math.radians(angle)))
        x3=int(r*math.cos(math.radians(angle)))
        LCD.pixel(cx-x3,cy+y3,cc)  # 4 quadrants
        LCD.pixel(cx-x3,cy-y3,cc)
        LCD.pixel(cx+x3,cy+y3,cc)
        LCD.pixel(cx+x3,cy-y3,cc)

def circle(x,y,r,c):
    LCD.hline(x-r,y,r*2,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i)) # Pythagoras!
        LCD.hline(x-a,y+i,a*2,c) # Lower half
        LCD.hline(x-a,y-i,a*2,c) # Upper half
    
def cubic_bezier(x1,y1,x2,y2,plotIter):
  x0 = 0
  y0 = 0

  x3 = 1
  y3 = 1
  
  def y(t):
    return math.pow(1 - t, 3) * y0 + 3 * math.pow(1 - t, 2) * t * y1 + 3 * (1 - t) * math.pow(t, 2) * y2 + math.pow(t, 3) * y3

  def x(t):
    return math.pow(1 - t, 3) * x0 + 3 * math.pow(1 - t, 2) * t * x1 + 3 * (1 - t) * math.pow(t, 2) * x2 + math.pow(t, 3) * x3

  resX = [];
  resY = [];

  m_range = (x * 1/plotIter for x in range(1, plotIter))
  for t in m_range:
        valX = x(t)
        valY = y(t)
        circle(int(30+valX*150),int(190-valY*150),2,colour(255,255,255))
        resY.append(valY)
  circle(180,40,2,colour(255,255,255))
  resY.append(1)
  return resY

# ==== Main ====  
pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(32768)#max 65535
### Initialize Screen
LCD = LCD_1inch3()

print("Initialize Screen")
report()
LCD.fill(LCD.RED)
LCD.show()

### Buffer
LCD.fill(0)
LCD.text("Cubic Bezier Demo",30,10,colour(255,0,0))
# y:40 - 190
# x:30 - 180
#LCD.hline(30,190,150,colour(0,0,255))
#LCD.vline(30,40,150,colour(0,255,0))
LCD.show()
print("After GFX demo")
report()

#utime.sleep(2)
white = 0xFFFF
LCD.text("Buffer: "+str(320*240*2) +" bytes",30,220,white)

LCD.show()
#utime.sleep(2)
red=colour(255,0,0)
green = colour(0,255,0)

LCD.fill_rect(30,220,190,8,0)
LCD.text("Press btns to tweak",30,220,white)

LCD.show()

### Set up buttons
key0 = Pin(15,Pin.IN,Pin.PULL_UP)
key1 = Pin(3,Pin.IN,Pin.PULL_UP)
key2 = Pin(17 ,Pin.IN,Pin.PULL_UP)
key3 = Pin(2 ,Pin.IN,Pin.PULL_UP)

panelBGCol = 0xffff00
LCD.fill_rect(220,0,100,240,panelBGCol)
keyText=['x1','y1','x2','y2']
keyValue=[0.50,0.50,0.50,0.50]
triggered = False
running = True
keyBorder = 3
xx = 260
yy = 15
plotIter = 80


while running:
    t = 0
    
    def downChange(i):
        index=i
        LCD.fill_rect(xx-30,yy+5+60*index,80,30,panelBGCol)
        
        if keyValue[index] < 1.0:
            keyValue[index] += 0.01
        else:
            keyValue[index] = 0.0
            
        LCD.text(keyText[index]+' - '+str(keyValue[index])[:4],xx-30,yy+5+60*index,white)
        LCD.fill_rect(230,40+60*index,int(80*keyValue[index]),keyBorder,green)
        
        # clean & draw bezier canvas
        LCD.fill_rect(10,20,200,190,0xff0000)
        cubic_bezier(keyValue[0],keyValue[1],keyValue[2],keyValue[3],plotIter)
        triggered = True
        
    def upChange(i):
        index=i
        LCD.text(keyText[index]+' - '+str(keyValue[index])[:4],xx-30,yy+5+60*index,white)
        LCD.fill_rect(230,40+60*index,int(80*keyValue[index]),keyBorder,white) 
        if triggered == False:
            cubic_bezier(keyValue[0],keyValue[1],keyValue[2],keyValue[3],plotIter)
     
    
    if key0.value() == 0:
        t = t + 1
               
    if(key1.value() == 0):
        t = t + 2          
                
    if(key2.value() == 0):
        t = t + 4
        
    if(key3.value() == 0):
        t = t + 8

    if t == 0: 
        upChange(0)
        upChange(1)
        upChange(2)
        upChange(3)
    if t == 1:
        downChange(0)
    if t == 2:
        downChange(1)
    if t == 4:
        downChange(2)
    if t == 8:
        downChange(3)
    if t == 15:
        print('trigger')
        iter = 60
        transition = cubic_bezier(keyValue[0],keyValue[1],keyValue[2],keyValue[3],int(iter))
        print(transition)
        for t in range(iter):
            LCD.fill_rect(30,201,160,8,0x000000) 
            LCD.fill_rect(int(30+transition[int(t)]*150),201,8,8,green)
            LCD.show()
    
    # control handle
    LCD.line(30,190,int(30+keyValue[0]*150),int(40+(1-keyValue[1])*150),colour(255,255,0))
    LCD.line(180,40,int(30+keyValue[2]*150),int(40+(1-keyValue[3])*150),colour(255,255,0))
    circle(int(30+keyValue[0]*150),int(40+(1-keyValue[1])*150),4,0xffff00)
    circle(int(30+keyValue[2]*150),int(40+(1-keyValue[3])*150),4,0xffff00)
    
    # border box
    LCD.hline(30,190,150,colour(0,0,255))
    LCD.hline(30,189,150,colour(0,0,255))
    LCD.hline(30,188,150,colour(0,0,255))
    LCD.vline(30,40,150,colour(0,255,0))
    LCD.vline(31,40,150,colour(0,255,0))
    LCD.vline(32,40,150,colour(0,255,0))
    LCD.hline(30,40,150,colour(180,180,180))
    LCD.hline(30,39,150,colour(180,180,180))
    LCD.hline(30,38,150,colour(180,180,180))
    LCD.vline(180,38,153,colour(180,180,180))
    LCD.vline(181,38,153,colour(180,180,180))
    LCD.vline(182,38,153,colour(180,180,180))
    
    LCD.show()    
               
