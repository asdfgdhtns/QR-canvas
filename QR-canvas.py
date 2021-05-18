import pygame
import math
import random
import sys

pygame.init()

codeScale = 20 # size of dots in pixels
BORDER = codeScale * 2
SIZE = 2*BORDER + codeScale*37


EClevel = 1 # low error correction
mask = 0
message = "Hello, World!"
dotArray = [[False for x in range(37)] for y in range(37)]
formatINT = 0
nDatawords = 108
nECwords = 26
codeWords = [0 for x in range(nDatawords + nECwords)]
init = 3 # when reloading code: 3-random background, 2-black background, 1-white background, 0-don't change background

def drawBigAllignment(x,y): # prints a big allignment square to dot array at x,y
    for a in range(7):
        dotArray[x+a][y]   = True
        dotArray[x+a][y+6] = True
        dotArray[x][y+a]   = True
        dotArray[x+6][y+a] = True
    for a in range(2,5):
        for b in range(2,5):
            dotArray[x+a][y+b] = True
def drawSmallAllignment(x,y): # prints a small allignment square to dot array at x,y
    dotArray[x][y]=True
    dotArray[x+1][y]=True
    dotArray[x+2][y]=True
    dotArray[x+3][y]=True
    dotArray[x+4][y]=True
    dotArray[x][y+4]=True
    dotArray[x+1][y+4]=True
    dotArray[x+2][y+4]=True
    dotArray[x+3][y+4]=True
    dotArray[x+4][y+4]=True
    dotArray[x][y+1]=True
    dotArray[x][y+2]=True
    dotArray[x][y+3]=True
    dotArray[x+4][y+1]=True
    dotArray[x+4][y+2]=True
    dotArray[x+4][y+3]=True
    dotArray[x+2][y+2]=True
def drawTiming():    # prints timing pattern to dot array
    for a in range(8,29,2):
        dotArray[a][6] = True
        dotArray[6][a] = True
    dotArray[8][29] = True
def isDataSpot(x,y): # returns true if pixel x,y in dot array holds message data
    if x==6 or y==6: # pixel is on the timing pattern or calibration square
        return False
    if x<9 and y<9:   # pixel is on calibration square or format
        return False
    if x<9 and y>28:  # pixel is on calibration square or format
        return False
    if x>28 and y<9:  # pixel is on calibration square of format
        return False
    if x>27 and y>27 and x<33 and y<33: #pix is on small calibration square
        return False
    if x<0:
        return False
    if x>36:
        return False
    if y<0:
        return False
    if y>36:
        return False
    
    return True
def calcData():      # fills codeWords[] with data from message string
    cPos = 0
    def addData(value, bits):
        nonlocal cPos
        for a in range(bits):
            codeWords[cPos>>3] |= 128>>(cPos&7)
            if not (value&(1<<bits-a-1)):
                codeWords[cPos>>3] ^= 128>>(cPos&7)
            cPos += 1
    addData(4,4) # binary mode
    addData(len(message),8)
    for a in range(len(message)):
        addData(ord(message[a]),8)
    addData(0,4)
def calcEC():        # calculates and adds Error Correction bytes to codeWords[]
    CGP = [0 for x in range(26)]
    R = [0 for a in range(109)] # 109 is number of data code words + 1
    def prod(n1,n2):
        p = 0
        
        for a in range(8):
            if n1&(1<<a):
                for b in range(8):
                    if (n2&(1<<b)):
                        p ^= 1<<(a+b)
        
        for a in range(14,7,-1):
            if p&(1<<a):
                p ^= 285<<(a-8)
        return p
    def polyProd(p1,d1,p2,d2):
        tp=[0 for x in range(27)] # 27 is number of EC coce words + 1
        
        for a in range(d1+1):
            if p1[a]:
                for b in range(d2+1):
                    if p2[b]:
                        tp[a+b] ^= prod(p1[a],p2[b])
        
        return tp
    def calcCGP():
        nonlocal CGP
        tp = [0 for a in range(27)] # 27 is number of EC code words + 1
        CGP[0] = 1
        CGP[1] = 1
        tp[0] = 1
        tp[1] = 2
        
        for a in range(1, nECwords):
            CGP = polyProd(CGP,a,tp,1)
            tp[1] = prod(tp[1],2)
    calcCGP()
    for a in range(nDatawords):
        R[a] = codeWords[a]
    
    R[nDatawords] = 0
    
    for a in range(nDatawords):
        c = R[0]
        for b in range(nECwords+1):
            if b < nECwords:
                R[b] = R[b+1]^prod(CGP[b+1],c)
            else:
                if a + nECwords < nDatawords:
                    R[b] = codeWords[a+nECwords+1]
                else:
                    R[b]=0
    for a in range(nECwords):
        codeWords[nDatawords + a] = R[a]
def calcFormat():    # calculates format bits and adds them to the formatINT
    global formatINT
    formatINT = EClevel << 13
    formatINT |= (mask  << 10)
    
    r = formatINT
    for a in range(4,-1,-1):
        if r&(1<<(a+10)):
            r ^= (1335 << a)
    formatINT|= r
    formatINT ^= 21522 # 21522 defined by densowave
def drawData():      # prints codeWords[] data to the dot array
    x = 36
    y = 36
    p = 0
    src = 0 # 0 = data, 1 = EC
    pByte = 0
    pBit = 0
    
    while p<4:
        #print(f'{pByte}, {pBit}, {x:2}, {y:2}, {isDataSpot(x,y)}')
        #clock.tick(50)
        if isDataSpot(x,y):
            if src == 0:
                dotArray[x][y] = False
                if codeWords[pByte] & (128>>pBit):
                    dotArray[x][y] = True
                pBit += 1
                if pBit == 8:
                    pBit = 0
                    pByte += 1
                    if pByte >= nDatawords:
                        pByte = 0
                        src = 1
            else:
                dotArray[x][y] = False
                if codeWords[nDatawords + pByte] & (128 >> pBit):
                    dotArray[x][y] = True
                pBit += 1
                if pBit == 8:
                    pBit = 0
                    pByte += 1
                    if pByte >= nECwords:
                        p=4
        if p == 0:
            x -= 1
            p = 1
        elif p == 1:
            x += 1
            p = 0
            if y == 0:
                x -= 2
                if x == 6:
                    x -= 1
                p = 2
            else:
                y -= 1
        elif p == 2:
            x -= 1
            p = 3
        elif p == 3:
            x += 1
            p = 2
            if y == 36:
                x -= 2
                p = 0
            else:
                y += 1
def readData():      # reads the dot array and converts to bytes, stores to codeWords[]
    x = 36
    y = 36
    p = 0
    pByte = 0
    pBit = 0
    
    while p<4:
        if isDataSpot(x,y):
            codeWords[pByte] |= (128>>pBit)
            if not dotArray[x][y]:
                codeWords[pByte] ^= (128>>pBit)
            pBit += 1
            if pBit == 8:
                pBit = 0
                pByte += 1
                if pByte >= nDatawords:
                    pByte = 0
                    p = 4
        if p == 0:
            x -= 1
            p = 1
        elif p == 1:
            x += 1
            p = 0
            if y == 0:
                x -= 2
                if x == 6:
                    x -= 1
                p = 2
            else:
                y -= 1
        elif p == 2:
            x -= 1
            p = 3
        elif p == 3:
            x += 1
            p = 2
            if y == 36:
                x -= 2
                p = 0
            else:
                y += 1
def drawFormat():    # prints the formatINT bits to the dot array
    fp=[[[8,8,8,8,8,8,8,8,7,5,4,3,2,1,0],[0,1,2,3,4,5,7,8,8,8,8,8,8,8,8]],[[36,35,34,33,32,31,30,29,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,8,30,31,32,33,34,35,36]]]
    for a in range(14,-1,-1):
        if formatINT & (1<<a):
            dotArray[fp[0][0][a]][fp[0][1][a]] = True
            dotArray[fp[1][0][a]][fp[1][1][a]] = True
        else:
            dotArray[fp[0][0][a]][fp[0][1][a]] = False;
            dotArray[fp[1][0][a]][fp[1][1][a]] = False;
def maskData():      # applies the mask to the dot array
    for x in range(37):
        for y in range(37):
            if isDataSpot(x,y):
                if mask == 0:
                    if ((x+y)&1) == 0:
                        dotArray[x][y]^=1
                elif mask == 1:
                    if (y&1) == 0:
                        dotArray[x][y]^=1
                elif mask == 2:
                    if (x%3) == 0:
                        dotArray[x][y]^=1
                elif mask == 3:
                    if ((x+y)%3) == 0:
                        dotArray[x][y]^=1
                elif mask == 4:
                    if ((y//2)+(x//3))&1 == 0:
                        dotArray[x][y]^=1
                elif mask == 5:
                    if (((x*y)&1)+((x*y)%3)) == 0:
                        dotArray[x][y]^=1
                elif mask == 6:
                    if ((((x*y)&1)+((x*y)%3))&1) == 0:
                        dotArray[x][y]^=1
                elif mask == 7:
                    if ((((x+y)%2)+((x*y)%3))%2) == 0 :
                        dotArray[x][y]^=1
def printCode():     # prints the dotArray to the pygame window
    for x in range(37):
        for y in range(37):
            if (dotArray[x][y]):
                pygame.draw.rect(screen, (0,0,0), (BORDER+x*codeScale, BORDER+y*codeScale, codeScale, codeScale))
            else:
                pygame.draw.rect(screen, (255,255,255), (BORDER+x*codeScale, BORDER+y*codeScale, codeScale, codeScale))
def reload():        # recalculates the code and draws it to the dot array (background affected by init variable)
    global init
    if init:
        if init == 1:
            for a in range(nDatawords):
                codeWords[a] = 0
        elif init == 2:
            for a in range(nDatawords):
                codeWords[a] = 255
        elif init == 3:
            for a in range(nDatawords):
                codeWords[a] = random.randint(0,255)
        drawData()
        maskData()
        readData()
    init = 0
    
    calcData()
    calcEC()
    drawData()
    calcFormat()
    drawFormat()
    maskData()
    printCode()
    
# initialize window and inital code

screen = pygame.display.set_mode((SIZE, SIZE))
screen.fill((255,255,255))
drawBigAllignment(0,0)
drawBigAllignment(0,30)
drawBigAllignment(30,0)
drawSmallAllignment(28,28)
drawTiming()
reload()
pygame.display.update()

print(f"\nMessage: {message}\nMask: {mask}\n\nKey commands:\n n: New message\n m: change Mask\n c: Clear background\n f: Fill background\n r: Random background")

# cursor variables

oldx = 0
oldy = 0
newx = 0
newy = 0

px = False # stores what color dot is being drawn to the screen

mode = 0 #cursor: 0-not pressed, 1-bad pix, 2-good pix

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                message = input("Message: ")
                reload()
                pygame.display.update()
            elif event.key == pygame.K_m:
                nMask = input("Mask (0 - 7): ")
                if len(nMask) == 1:
                    if int(nMask[0]) >= 0 and int(nMask[0]) <= 7:
                        mask = int(nMask[0])
                        maskData()
                        readData()
                        reload()
                        pygame.display.update()
            elif event.key == pygame.K_c:
                init = 1 # clear background
                reload()
                pygame.display.update()
            elif event.key == pygame.K_f:
                init = 2 # black background
                reload()
                pygame.display.update()
            elif event.key == pygame.K_r:
                init = 3 # random background
                reload()
                pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            newx = (event.pos[0]-BORDER)//codeScale # math converts mouse x and y to dot array x and y
            newy = (event.pos[1]-BORDER)//codeScale
            if isDataSpot(newx, newy):
                mode = 2 # user clicked on a good pixel
                px = not dotArray[newx][newy]
                dotArray[newx][newy] = px
                printCode()
                maskData()
                readData()
                calcData()
                calcEC()
                drawData()
                maskData()
                printCode()
                pygame.display.update()
            else:
                mode = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            mode = 0
        elif event.type == pygame.MOUSEMOTION:
            if mode == 2: # if the user is clicking on a changable pixel
                oldx = newx
                oldy = newy
                newx = (event.pos[0]-BORDER)//codeScale
                newy = (event.pos[1]-BORDER)//codeScale
                
                if oldx != newx or oldy != newy: # if the mouse was moved to another pixel
                    oldx = newx
                    oldy = newy
                    if isDataSpot(oldx, oldy):
                        dotArray[oldx][oldy] = px
                        printCode()
                        maskData()
                        readData()
                        calcData()
                        calcEC()
                        drawData()
                        maskData()
                        printCode()
                        pygame.display.update()
