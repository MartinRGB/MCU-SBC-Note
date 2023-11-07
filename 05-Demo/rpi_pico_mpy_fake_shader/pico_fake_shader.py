# WS 320x240 display example
from machine import Pin,SPI,PWM,Timer
import framebuf
import utime
import os
import gc
import math
import random

oc_freq = 270000000

machine.freq(oc_freq)
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

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

class Vector2:
    """A two-dimensional vector with Cartesian coordinates."""

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        """Human-readable string representation of the vector."""
        return '{:g}i + {:g}j'.format(self.x, self.y)

    def __repr__(self):
        """Unambiguous string representation of the vector."""
        return repr((self.x, self.y))

    def dot(self, other):
        """The scalar (dot) product of self and other. Both must be vectors."""

        if not isinstance(other, Vector2D):
            raise TypeError('Can only take dot product of two Vector2D objects')
        return self.x * other.x + self.y * other.y
    # Alias the __matmul__ method to dot so we can use a @ b as well as a.dot(b).
    __matmul__ = dot

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector2(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """Vector addition."""
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """Multiplication of a vector by a scalar."""

        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vector2(self.x*scalar, self.y*scalar)
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __rmul__(self, scalar):
        """Reflected multiplication so vector * scalar also works."""
        return self.__mul__(scalar)

    def __neg__(self):
        """Negation of the vector (invert through origin.)"""
        return Vector2(-self.x, -self.y)

    def __truediv__(self, scalar):
        """True division of the vector by a scalar."""
        return Vector2(self.x / scalar, self.y / scalar)

    def __mod__(self, scalar):
        """One way to implement modulus operation: for each component."""
        return Vector2(self.x % scalar, self.y % scalar)

    def __abs__(self):
        """Absolute value (magnitude) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, other):
        """The distance between vectors self and other."""
        return abs(self - other)

    def to_polar(self):
        """Return the vector's components in polar coordinates."""
        return self.__abs__(), math.atan2(self.y, self.x)

class LCD_2inch(framebuf.FrameBuffer):
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
        """Initialize dispaly"""  
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

# ==== some shader function ====
def fract(x):
    return x - math.floor(x)

def dot(v1, v2):
    return sum(x*y for x, y in zip(v1, v2))

def random1(x):
    #return random.random()
    return fract(math.sin(x)*1e4);

def random2(x):
    return fract(math.sin(dot(x, [12.9898,78.233]))* 43758.5453123);

def step(a,b):
    if(a<b):
        return 0
    else:
        return 1

def pattern(st,v,t):
    vx =math.floor(st.x+v.x)
    vy =math.floor(st.y+v.y)
    p=Vector2(vx,vy)
    return step(t, random2([100.+p.x*.000001,100.+p.y*.000001])+random1(p.x)*0.5 )

def smoothstep (edge0, edge1,  x):
   clampeVal = (x - edge0) / (edge1 - edge0)
   clampedVal = max(0.,min(1.,clampeVal))
   return x * x * (3.0 - 2.0 * x)


def smoothen(d1,d2):
    k = 1.5;
    return -math.log(math.exp(-k * d1) + math.exp(-k * d2)) / k;

# ==== variable ====

white = colour(255,255,255)
red=colour(255,0,0)
green = colour(0,255,0)
blue = colour(255,255,255)

# ==== Main ====  
pwm = PWM(Pin(BL))
pwm.freq(10000)
pwm.duty_u16(65535)#max 65535
### Initialize Screen
LCD = LCD_2inch()


print("Initialize Screen")
report()
LCD.fill(LCD.RED)
LCD.show()

### Buffer

LCD.fill(0)
LCD.text("Fake GLSL Demo",104,20,colour(255,0,0))
LCD.show()
print("After GFX demo")
report()
LCD.text("Buffer: "+str(320*240*2) +" bytes",80,210,white)
LCD.rect(70,46,180,141,colour(255,255,255))
for i in range(0,24):
    LCD.fill_rect(100+i*5,116,5,8,colour(255- i*10,255,255-i*10))
    LCD.show()
    
LCD.show()

### Subtitle
utime.sleep(1.5)
LCD.fill(0)
LCD.rect(70,46,181,141,colour(255,255,255))
LCD.text("Fake GLSL Demo",104,20,colour(255,0,0))

### Fake Shader
sampleScale = 0.07
sW = 320 * sampleScale
sH = 240 * sampleScale
         
cX=0
cY=0

#LCD.text("Fake GLSL Demo",104,20,colour(0,255,0))
LCD.text("Press btns to tweak",84,210,white)

LCD.show()


#### Init the UV Shader


for pY in range(sH):
    for pX in range(sW):
        uv=Vector2(pX/sW,1.-pY/sH) 
        c = colour(int(uv.x*255),int(uv.y*255),int(0.*255))
        w = h = int((1/sampleScale)/2)
        LCD.fill_rect(80+pX*w,56+pY*h, w,h,c)
    LCD.show()

LCD.fill_rect(80,20,181,8,colour(0,0,0))  
LCD.text("Basic Gradient",104,20,colour(0,255,0))
LCD.text("Press btns to tweak",84,210,white)

LCD.show()


### Set up buttons
key0 = Pin(15,Pin.IN,Pin.PULL_UP)
key1 = Pin(3,Pin.IN,Pin.PULL_UP)
key2 = Pin(17 ,Pin.IN,Pin.PULL_UP)
key3 = Pin(2 ,Pin.IN,Pin.PULL_UP)

running = True

gradV = 0;

prevBtn = -1;

while running:
    t = 0
    isUpdate = False;
    
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    
    
    if key0.value() == 0:
        t = t + 1
        cX = cX + 0.05
    if(key1.value() == 0):
        t = t + 2
        cY = cY + 0.05
    if(key2.value() == 0):
        t = t + 4
        cX = cX - 0.05
    if(key3.value() == 0):
        t = t + 8
        cY = cY - 0.05

    if t == 0:
        isUpdate = False
    
    if t == 1:
        print('1 down')
        isUpdate = True;
        # Basic Gradient
        gradV += 10
        if(gradV > 255):
            gradV = 0
        LCD.fill_rect(80,20,180,8,colour(0,0,0))  
        LCD.text("Basic Gradient",104,20,colour(0,255,0))
        for pY in range(sH):
            for pX in range(sW):
                uv=Vector2(pX/sW,1.-pY/sH) 
                c = colour(int(uv.x*255),int(uv.y*255),int(gradV))
                w = h = int((1/sampleScale)/2)
                LCD.fill_rect(80+pX*w,56+pY*h, w,h,c)
            if prevBtn != 0:
                LCD.show()
        prevBtn = 0

    if t == 2:
        print('2 down')
        isUpdate = True;
        # Voronoi - https://thebookofshaders.com/12/
        LCD.fill_rect(80,20,180,8,colour(0,0,0))
        LCD.text("Voronoi",126,20,colour(0,255,0))
        for pY in range(sH):
            for pX in range(sW):
                uv=Vector2(pX/sW,1.-pY/sH)
                
                uv.x *= sW/sH

                scale = 3
                uv.x *= scale
                uv.y *= scale

                i_st = Vector2(math.floor(uv.x),math.floor(uv.y));
                f_st = Vector2(fract(uv.x),fract(uv.y));
            
                m_dist = 1.
                
                for iy in range(-1,2): # -1,2 is slow
                    for ix in range(-1,2): # -1.2 is slow
                        neighbor = Vector2(ix,iy)
                        point = random2([i_st.x+neighbor.x,i_st.y+neighbor.y]);
                        point = 0.5 + 0.5*math.sin(cY*10.+6.2831*point);
                        diff = Vector2(neighbor.x + point - f_st.x,neighbor.y + point - f_st.y);
                        dist = math.sqrt(diff.x*diff.x+diff.y*diff.y)
                        m_dist = min(m_dist, dist);
                w = h = int((1/sampleScale)/2)
                c = colour(int(m_dist*255*0),int(m_dist*255*0),int(m_dist*255))
                LCD.fill_rect(80+pX*w,56+pY*h, w,h,c)
            if prevBtn != 1:
                    LCD.show()
        
        prevBtn = 1
    if t == 4:
        print('3 down')
        isUpdate = True;
        LCD.fill_rect(80,20,180,8,colour(0,0,0))
        LCD.text("WaterColor",118,20,colour(0,255,0))
        # WaterColor - https://www.shadertoy.com/view/lsyfWD
        for pY in range(sH):
            for pX in range(sW):
                uv=Vector2(pX/sW,1.-pY/sH) 
                #LCD.pixel(pX*4,pY*4,colour(int(uv.x*255),int(uv.y*255),a))
                speed = .1;
                scale = 0.15;
                p = Vector2(pX*scale,pY*scale)   
                for i in range(1,4):
                    p.x+=0.3/i*math.sin(i*3.*p.y) + cX;
                    p.y+=0.3/i*math.cos(i*3.*p.x) + cY;
                r=math.cos(p.x+p.y+1.)*.5+.5;
                g=math.sin(p.x+p.y+1.)*.5+.5;
                b=(math.sin(p.x+p.y)+math.cos(p.x+p.y))*.3+.5;
                
                c = colour(int(r*255),int(g*255),int(b*255))
                w = h = int((1/sampleScale)/2)
                LCD.fill_rect(80+pX*w,56+pY*h, w,h,c)
                #LCD.fill_rect(pX,pY,1,1,c)
            if prevBtn != 2:
                LCD.show()
        
        prevBtn = 2
    if t == 8:
        print('4 down')
        isUpdate = True;
        LCD.fill_rect(80,20,180,8,colour(0,0,0))
        LCD.text("SDF Metaball",114,20,colour(0,255,0))
        # SDF Metalball - https://thebookofshaders.com/edit.php?log=160414040804
        for pY in range(sH):
            for pX in range(sW):
                uv = Vector2(pX/sW,1.-pY/sH) 
                p0 = Vector2(1.5*math.cos(cY*2.) + 0.48, 0.53);
                p1 = Vector2(-1.5*math.cos(cY*2.) + 0.5, 0.53);
                la = math.sqrt((uv.x-p0.x)*(uv.x-p0.x) + (uv.y-p0.y)*(uv.y-p0.y))
                lb = math.sqrt((uv.x-p1.x)*(uv.x-p1.x) + (uv.y-p1.y)*(uv.y-p1.y))
                d = smoothen(la * 3,lb*3);
                ae = 5.0 / sH
                color = smoothstep(0.8, 0.8+ae, d*(sampleScale*8))
                c = colour(int(255-color*255),int(255-color*255),int(255-color*255))
                w = h = int((1/sampleScale)/2)
                LCD.fill_rect(80+pX*w,56+pY*h, w,h,c)
            if prevBtn != 3:
                LCD.show()
        prevBtn = 3
    if t == 15:
        print('all down')
    if isUpdate == True:
            LCD.show()
    
    LCD.fill_rect(10,20, 60,8,colour(0,0,0))
    LCD.text("T: " + str(temperature)[:4],10,20,colour(255,255,0))
    
    LCD.show()    
               
