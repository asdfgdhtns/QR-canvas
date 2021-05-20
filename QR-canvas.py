import pygame
import math
import random
import sys

pygame.init()
#clock = pygame.time.Clock()

version = 32
codeScale = 10 # size of dots in pixels

EClevel = 1 # low error correction
mask = 0
message = "Hello, World!"
aPatLoc = [[0],[0],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46],[6,28,50],[6,30,54],[6,32,58],[6,34,62],[6,26,46,66],[6,26,48,70],[6,26,50,74],[6,30,54,78],[6,30,56,82],[6,30,58,86],[6,34,62,90],[6,28,50,72,94],[6,26,50,74,98],[6,30,54,78,102],[6,28,54,80,106],[6,32,58,84,110],[6,34,62,90,118],[6,30,58,86,114],[6,26,50,74,98,122],[6,30,54,78,102,126],[6,26,52,78,104,130],[6,30,56,82,108,134],[6,34,60,86,112,138],[6,30,58,86,114,142],[6,34,62,90,118,146],[6,30,54,78,102,126,150],[6,24,50,76,102,128,154],[6,28,54,80,106,132,158],[6,32,58,84,110,136,162],[6,26,54,82,110,138,166],[6,30,58,86,114,142,170]]
aPatCnt = [0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7]
dotArray = [[False for x in range(17 + version * 4)] for y in range(17 + version * 4)]
formatINT = 0
versionINT = 0
nDatawords = [[0, 19, 34, 55, 80, 108, 68, 78, 97, 116, 68, 81, 92, 107, 115, 87, 98, 107, 120, 113, 107, 116, 111, 121, 117, 106, 114, 122, 117, 116, 115, 115, 115, 115, 115, 121, 121, 122, 122, 117, 118],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 69, 0, 93, 0, 116, 88, 99, 108, 121, 114, 108, 117, 112, 122, 118, 107, 115, 123, 118, 117, 116, 116, 0, 116, 116, 122, 122, 123, 123, 118, 119]] # number of data words per block in each version
nECwords = [0, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30] # number of error correction words per block in each version
nBlocks = [[0, 1, 1, 1 ,1, 1, 2, 2, 2, 2, 2, 4, 2, 4, 3, 5, 5, 1, 5, 3, 3, 4, 2, 4, 6, 8, 10, 8, 3, 7, 5, 13, 17, 17, 13, 12, 6, 17, 4, 20, 19],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 1, 1, 1, 5, 1, 4, 5, 4, 7, 5, 4, 4, 2, 4, 10, 7, 10, 3, 0, 1, 6, 7, 14, 4, 18, 4, 6]] # number of blocks in each version
#          0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40
nGroups = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2]
codeWords = [[[0 for x in range(5000)] for y in range(5000)] for z in range(2)] # FIX THIS
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
    dotArray[x-2][y-2]=True
    dotArray[x-1][y-2]=True
    dotArray[x  ][y-2]=True
    dotArray[x+1][y-2]=True
    dotArray[x+2][y-2]=True
    dotArray[x-2][y+2]=True
    dotArray[x-1][y+2]=True
    dotArray[x  ][y+2]=True
    dotArray[x+1][y+2]=True
    dotArray[x+2][y+2]=True
    dotArray[x-2][y-1]=True
    dotArray[x-2][y  ]=True
    dotArray[x-2][y+1]=True
    dotArray[x+2][y-1]=True
    dotArray[x+2][y  ]=True
    dotArray[x+2][y+1]=True
    dotArray[x  ][y  ]=True
def drawTiming():    # prints timing pattern to dot array
    for a in range(8, 8 + version * 4,2):
        dotArray[a][6] = True
        dotArray[6][a] = True
    dotArray[8][8 + version * 4] = True
def isDataSpot(x,y): # returns true if pixel x,y in dot array holds message data
    
    # pixel is off the code
    
    if x < 0:
        return False
    if x >= 17 + version * 4:
        return False
    if y < 0:
        return False
    if y >= 17 + version * 4:
        return False
    
    # Pixel is on a function pattern
    
    if x == 6 or y == 6: # pixel is on the timing pattern or calibration square
        return False
    if x < 9 and y < 9:   # pixel is on calibration square or format
        return False
    if x < 9 and y > (17+4*version) - 9:  # pixel is on calibration square or format
        return False
    if x > (17+4*version) - 9 and y < 9:  # pixel is on calibration square of format
        return False
    for a in range(aPatCnt[version]):
        for b in range(aPatCnt[version]):
            if not ((a == 0 and b == 0) or (a == 0 and b == aPatCnt[version] - 1) or (a == aPatCnt[version] - 1 and b == 0)):
                if (x >= aPatLoc[version][a] -2 and x <= aPatLoc[version][a] + 2 and y >= aPatLoc[version][b] - 2 and y <= aPatLoc[version][b] + 2):
                    return False # pixel is on a small allignment pattern
    if version > 6:
        if y < 6 and x > 5 + version * 4:
            return False #pixel is on bottom right version block
        if x < 6 and y > 5 + version * 4:
            return False #pixel is on bottom right version block
    
    return True
def calcData():      # fills codeWords[] with data from message string
    b = 0
    g = 0
    cPos = 0
    def addData(value, bits):
        nonlocal cPos
        nonlocal b
        nonlocal g
        for a in range(bits):
            codeWords[g][b][cPos>>3] |= 128>>(cPos&7)
            if not (value&(1<<bits-a-1)):
                codeWords[g][b][cPos>>3] ^= 128>>(cPos&7)
            cPos += 1
            if cPos>>3 == nDatawords[g][version]:
                cPos = 0
                b += 1
                if b == nBlocks[g][version]:
                    b = 0
                    g += 1
    
    addData(4,4) # binary mode
    if version < 10:
        addData(len(message),8)
    else:
        addData(len(message),16)
    for a in range(len(message)):
        addData(ord(message[a]),8)
    while cPos&7:
        addData(0,1)
def calcEC():        # calculates and adds Error Correction bytes to codeWords[]
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
        tp=[0 for x in range(nECwords[version]+1)]
        
        for a in range(d1+1):
            if p1[a]:
                for b in range(d2+1):
                    if p2[b]:
                        tp[a+b] ^= prod(p1[a],p2[b])
        
        return tp
    
    CGP = [0 for x in range(nECwords[version])]
    R = [0 for a in range(max(nDatawords[0][version], nDatawords[1][version]) + 1)]
    
    # calculate CGP
    tp = [0 for a in range(nECwords[version]+1)]
    CGP[0] = 1
    CGP[1] = 1
    tp[0] = 1
    tp[1] = 2
    
    for a in range(1, nECwords[version]):
        CGP = polyProd(CGP,a,tp,1)
        tp[1] = prod(tp[1],2)
    
    for g in range(nGroups[version]):
        for b in range(nBlocks[g][version]):
            for a in range(nDatawords[g][version]):
                R[a] = codeWords[g][b][a]
            
            R[nDatawords[g][version]] = 0
            
            for a in range(nDatawords[g][version]):
                c = R[0]
                for d in range(nECwords[version]+1):
                    if d < nECwords[version]:
                        R[d] = R[d+1]^prod(CGP[d+1],c)
                    elif a + nECwords[version] < nDatawords[g][version]:
                        R[d] = codeWords[g][b][a+nECwords[version]+1]
                    else:
                        R[d]=0
            for a in range(nECwords[version]):
                codeWords[g][b][nDatawords[g][version] + a] = R[a]
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
def calcVersion():   # calculates version bits and adds them to the versionINT
    global versionINT
    if version > 6:
        versionINT = version << 12
        r = versionINT
        for a in range(5,-1,-1):
            if r&(1<<(a+12)):
                r ^= (7973 << a)
        versionINT|= r
def drawData():      # prints codeWords[] data to the dot array
    x = y = 16 + version * 4
    p = 0 # 0-right side going up, 1- left side going up, 2-right side going down, 3-left side going down
    b = 0 # what block we are on
    g = 0 # what group we are on
    pByte = 0 # position in byte list
    pBit = 0 # position of bit in byte
    
    while p<4:
        #print(f'{pByte}, {pBit}, {x:2}, {y:2}, {isDataSpot(x,y)}')
        #clock.tick(50)
        if isDataSpot(x,y):
            dotArray[x][y] = False
            if codeWords[g][b][pByte] & (128>>pBit):
                dotArray[x][y] = True
            pBit += 1
            if pBit == 8:
                pBit = 0
                b += 1
                if b == nBlocks[g][version]:
                    b = 0
                    g += 1
                    #print(" ", g, " ", nGroups[version])
                    if g == nGroups[version]:
                        g = 0
                        if nGroups[version] == 2 and pByte == nDatawords[0][version] - 1:
                            g = 1
                        pByte += 1
                        if pByte == max(nDatawords[0][version], nDatawords[1][version]) + nECwords[version]:
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
            if y == 16 + version * 4:
                x -= 2
                p = 0
            else:
                y += 1
def readData():      # reads the dot array and converts to bytes, stores to codeWords[]
    x = y = 16 + version * 4
    p = 0 # 0-right side going up, 1- left side going up, 2-right side going down, 3-left side going down
    b = 0 # what block we are on
    g = 0 # what group we are on
    pByte = 0 # position in byte list
    pBit = 0 # position of bit in byte
    
    while p<4:
        #print(f'{pByte}, {pBit}, {x:2}, {y:2}, {isDataSpot(x,y)}')
        #clock.tick(50)
        if isDataSpot(x,y):
            codeWords[g][b][pByte] |= (128>>pBit)
            if not dotArray[x][y]:
                codeWords[g][b][pByte] ^= (128>>pBit)
            pBit += 1
            if pBit == 8:
                #print(f'{pByte:3}, {g}, {b:2}');
                pBit = 0
                b += 1
                if b == nBlocks[g][version]:
                    b = 0
                    g += 1
                    if g == nGroups[version]:
                        g = 0
                        if nGroups[version] == 2 and pByte == nDatawords[0][version] - 1:
                            g = 1
                        pByte += 1
                        if pByte == max(nDatawords[0][version], nDatawords[1][version]) + nECwords[version]:
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
            if y == 16 + version * 4:
                x -= 2
                p = 0
            else:
                y += 1
def drawFormat():    # prints the formatINT bits to the dot array
    o = 16 + version * 4
    fp=[[[8,8,8,8,8,8,8,8,7,5,4,3,2,1,0],[0,1,2,3,4,5,7,8,8,8,8,8,8,8,8]],[[o,o-1,o-2,o-3,o-4,o-5,o-6,o-7,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,8,o-6,o-5,o-4,o-3,o-2,o-1,o]]]
    for a in range(14,-1,-1):
        if formatINT & (1<<a):
            dotArray[fp[0][0][a]][fp[0][1][a]] = True
            dotArray[fp[1][0][a]][fp[1][1][a]] = True
        else:
            dotArray[fp[0][0][a]][fp[0][1][a]] = False;
            dotArray[fp[1][0][a]][fp[1][1][a]] = False;
def drawVersion():   # prints the versionINT bits to the dot array
    if version > 6:
        for a in range(3):
            for b in range(6):
                dotArray[6 + version * 4 + a][b] = False # top right version block
                dotArray[b][6 + version * 4 + a] = False # top left version block
                if versionINT & (1 << (17-(b*3+a))):
                    dotArray[6 + version * 4 + a][b] = True # top right version block
                    dotArray[b][6 + version * 4 + a] = True # top left version block
def maskData():      # applies the mask to the dot array
    for x in range(17 + version * 4):
        for y in range(17 + version * 4):
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
    for x in range(17 + version * 4):
        for y in range(17 + version * 4):
            if (dotArray[x][y]):
                pygame.draw.rect(screen, (0,0,0), (BORDER+x*codeScale, BORDER+y*codeScale, codeScale, codeScale))
            else:
                pygame.draw.rect(screen, (255,255,255), (BORDER+x*codeScale, BORDER+y*codeScale, codeScale, codeScale))
def reload():        # recalculates the code and draws it to the dot array (background affected by init variable)
    global init
    if init:
        if init == 1:
            for g in range(nGroups[version]):
                for a in range(nDatawords[g][version]):
                    for b in range(nBlocks[g][version]):
                        codeWords[g][b][a] = 0
        elif init == 2:
            for g in range(nGroups[version]):
                for a in range(nDatawords[g][version]):
                    for b in range(nBlocks[g][version]):
                        codeWords[b][a] = 255
        elif init == 3:
            for g in range(nGroups[version]):
                for a in range(nDatawords[g][version]):
                    for b in range(nBlocks[g][version]):
                        codeWords[g][b][a] = random.randint(0,255)
        drawData()
        maskData()
        readData()
    init = 0
    
    calcData()
    calcEC()
    drawData()
    calcFormat()
    drawFormat()
    calcVersion()
    drawVersion()
    maskData()
    printCode()

# initialize window and inital code

BORDER = codeScale * 2
SIZE = 2 * BORDER + codeScale * (17 + 4*version)
screen = pygame.display.set_mode((SIZE, SIZE))
screen.fill((255,255,255))

drawBigAllignment(0,0)
drawBigAllignment(0,10 + version * 4)
drawBigAllignment(10 + version * 4,0)
print("Version: ",version)
for a in range(aPatCnt[version]):
    print(aPatLoc[version][a])
    for b in range(aPatCnt[version]):
        if not ((a == 0 and b == 0) or (a == 0 and b == aPatCnt[version] - 1) or (a == aPatCnt[version] - 1 and b == 0)):
            drawSmallAllignment(aPatLoc[version][a], aPatLoc[version][b])
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
                dotArray[newx][newy] = px # change the pixel the user clicked
                #maskData()  # mask the code
                #readData()  # read the masked data
                #calcData()  # calculate code words of the masked data
                #calcEC()    # calculate the error correction bytes for masked data
                #drawData()  # draw the code words to the dot array
                #maskData()  # mask the masked data (which unmasks it back to what the user drew)
                printCode() # print it to the screen
                pygame.display.update()
            else:
                mode = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if mode == 2:
                maskData()
                readData()
                calcData()
                calcEC()
                drawData()
                maskData()
                printCode()
                pygame.display.update()
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
                        pygame.display.update()
