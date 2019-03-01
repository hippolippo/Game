import pygame
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from math import sin, cos, floor, ceil


def get_looking_at(xrot, yrot, xpos, ypos, zpos, blocks, reach):
    print(xpos,ypos,zpos)
    print(xrot,yrot)
    xrot, yrot = math.radians(xrot), math.radians(yrot)
    '''
    xlook = math.cos(xrot) * math.cos(yrot)
    ylook = (1-math.cos(yrot))**0.5
    zlook = math.cos(yrot) * math.sin(xrot)
    print(xlook,ylook,zlook)
    #Begin Trace
    #Trace X (east/west)
    xIntercepts = list()
    for x in range(reach):
        xl = x + round(xpos) + .5
        if xrot < 0 or xrot > math.pi:
            xl = -lx
            x = -x
        y = (x*ylook)/xlook + ypos
        z = (x*zlook)/xlook + zpos
        xIntercepts.append((xl,y,z))
    #Trace Y (top/bottom)
    yIntercepts = list()
    for y in range(reach):
        y = ypos + y
        y = math.ceil(y)
        if yrot < 0 or yrot > math.pi:
            y = -y
            
        x = (y*xlook)/ylook
        z = (y*zlook)/xlook
        yIntercepts.append((x,y,z))
    #Trace Z (north/south)
    zIntercepts = list()
    for z in range(reach):
        z = z + zpos
        z = round(z)
        z += .5
        if xrot < -math.pi/2 or xrot > math.pi/2:
            z = -z
        x = (z*xlook)/zlook
        y = (z*ylook)/zlook
        zIntercepts.append((x,y,z))
    if xrot > 0 and xrot < math.pi:
        xface = "West"
    else:
        xface = "East"
    if xrot > -math.pi/2 and xrot < math.pi/2:
        zface = "South"
    else:
        zface = "North"
    if yrot > 0 and yrot < math.pi:
        yface = "Top"
    else:
        yface = "Bottom"
    blocksDistance = dict()
    for i in xIntercepts:
        blocksDistance[sum(i)]=(i[0],i[1],i[2],xface)
    for i in yIntercepts:
        blocksDistance[sum(i)]=(i[0],i[1],i[2],yface)
    for i in zIntercepts:
        blocksDistance[sum(i)]=(i[0],i[1],i[2],zface)
    lookingAt = [(x,)+blocksDistance[x] for x in blocksDistance]'''
    xform = sin(xrot)*cos(yrot)+xpos
    yform = sin(yrot)+ypos
    zform = -(cos(xrot)*cos(yrot))+zpos
    xforward = xform-xpos >= 0
    yforward = yform-ypos >= 0
    zforward = zform-zpos >= 0
    if xforward:
        xset = [floor(x+xpos+.5)+.5 for x in range(reach)]
    else:
        xset = [floor((-x)+xpos+.5)-.5 for x in range(reach)]
    if yforward:
        yset = [ceil(y+ypos) for y in range(reach)]
    else:
        yset = [floor((-y)+ypos) for y in range(reach)]
    if zforward:
        zset = [floor(z+zpos+.5)+.5 for z in range(reach)]
    else:
        zset = [floor((-x)+xpos+.5)-.5 for x in range(reach)]
    xint = []
    yint = []
    zint = []
    for x in xset:
        y = ((yform-ypos)*x)/(xform-xpos)
        z = ((zform-zpos)*x)/(xform-xpos)
        xint.append((x, y+ypos, z+zpos))
    for y in yset:
        x = ((xform-xpos)*y)/(yform-ypos)
        z = ((zform-zpos)*y)/(yform-ypos)
        yint.append((x+xpos, y, z+zpos))
    for z in zset:
        x = ((xform-xpos)*z)/(zform-zpos)
        y = ((yform-ypos)*z)/(zform-zpos)
        zint.append((x+xpos,y+ypos,z))
    intercepts = dict()
    for pos in xint:
        intercepts[(pos[0]-xpos)**2+(pos[1]-ypos)**2+(pos[2]-zpos)**2] = (pos[0], pos[1], pos[2], "x")
    for pos in yint:
        intercepts[(pos[0]-xpos)**2+(pos[1]-ypos)**2+(pos[2]-zpos)**2] = (pos[0], pos[1], pos[2], "y")
    for pos in zint:
        intercepts[(pos[0]-xpos)**2+(pos[1]-ypos)**2+(pos[2]-zpos)**2] = (pos[0], pos[1], pos[2], "z")
    indices = [x for x in intercepts]
    indices.sort()
    for index in indices:
        connection = intercepts[index]
        print(connection)
        if xforward:
            x = floor(connection[0]+.5)
            xdir = "e"
        else:
            x = ceil(connection[0]-.5)
            xdir = "w"
        if yforward:
            y = floor(connection[1])
            ydir = "d"
        else:
            y = floor(connection[1])+1
            ydir = "u"
        if zforward:
            z = ceil(connection[2]-.5)
            zdir = "n"
        else:
            z = floor(connection[2]+.5)
            zdir = "s"
        print(x,y,z)
        try:
            if blocks.get_data(x, y, z) != None:
                if math.sqrt(index) <= reach:
                    if connection[3] == "x":
                        return x, y, z, xdir
                    if connection[3] == "y":
                        return x, y, z, ydir
                    if connection[3] == "z":
                        return x, y, z, zdir
                else:
                    return
            else:
                continue
        except IndexError:
            continue
    return


def render_area(x, y, z, area):
    for block in area.iterate():
        cube(block[0][0] - x, block[0][1] - y, block[0][2] - z, block[1])


def cube(x, y, z, color):
    glBegin(GL_QUADS)
    glColor3f(color[0][0], color[0][1], color[0][2])  # N
    glVertex3f(x + .5, y + 1, z + .5)
    glVertex3f(x - .5, y + 1, z + .5)
    glVertex3f(x - .5, y, z + .5)
    glVertex3f(x + .5, y, z + .5)
    glColor3f(color[1][0], color[1][1], color[1][2])  # S
    glVertex3f(x - .5, y + 1, z - .5)
    glVertex3f(x + .5, y + 1, z - .5)
    glVertex3f(x + .5, y, z - .5)
    glVertex3f(x - .5, y, z - .5)
    glColor3f(color[2][0], color[2][1], color[2][2])  # W
    glVertex3f(x + .5, y + 1, z - .5)
    glVertex3f(x + .5, y + 1, z + .5)
    glVertex3f(x + .5, y, z + .5)
    glVertex3f(x + .5, y, z - .5)
    glColor3f(color[3][0], color[3][1], color[3][2])  # E
    glVertex3f(x - .5, y + 1, z + .5)
    glVertex3f(x - .5, y + 1, z - .5)
    glVertex3f(x - .5, y, z - .5)
    glVertex3f(x - .5, y, z + .5)
    glColor3f(color[4][0], color[4][1], color[4][2])  # U
    glVertex3f(x + .5, y + 1, z - .5)
    glVertex3f(x - .5, y + 1, z - .5)
    glVertex3f(x - .5, y + 1, z + .5)
    glVertex3f(x + .5, y + 1, z + .5)
    glColor3f(color[5][0], color[5][1], color[5][2])  # D
    glVertex3f(x + .5, y, z - .5)
    glVertex3f(x + .5, y, z + .5)
    glVertex3f(x - .5, y, z + .5)
    glVertex3f(x - .5, y, z - .5)
    glEnd()


def crosshair(x, y, w):
    glColor3f(.8, .8, .8)
    glBegin(GL_LINES)
    glVertex2f(x-w, y)
    glVertex2f(x+w, y)
    glVertex2f(x, y-w)
    glVertex2f(x, y+w)
    glEnd()

def main(world,x,y,z,width,height,renderDistance,step):
    hand = [
        [0, 1, 0],
        [1, 0, 0],
        [1, 0, 1],
        [0, 0, 1],
        [1, 1, 0],
        [0, 1, 1]
    ]
    rightClicked = False
    leftClicked = False
    currentColor = (186, 243, 255)
    xrot = 0
    yrot = 0
    pygame.init()
    screen = pygame.display.set_mode((width,height), DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CCW)
    glShadeModel(GL_SMOOTH)
    glDepthRange(0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (width/height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    pygame.mouse.set_visible(False)
    facing = [0, 0, False]
    pressedKeys = {119:False,97:False,115:False,100:False,32:False,304:False,108:False}
    while True:
        newMousePos = pygame.mouse.get_pos()
        change = (newMousePos[0]-(width/2), newMousePos[1]-(height/2))
        pygame.mouse.set_pos([width / 2, height / 2])
        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        yrot -= change[1]*0.1
        glRotate(change[1]*0.1, 1, 0, 0)
        glMultMatrixf(modelview)
        xrot += change[0]*0.1
        glRotate(change[0]*0.1, 0, 1, 0)
        '''
        if yrot < -90:
            yrot = -90
            glRotate((yrot+90),1,0,0)
        if yrot > 90:
            yrot = 90
            glRotate((yrot-90),0,1,0)
            '''
        xmin = round(x-renderDistance[0])
        ymin = round(y-renderDistance[1])
        zmin = round(z-renderDistance[2])
        if xmin < 0:
            xmin = 0
        if ymin < 0:
            ymin = 0
        if zmin < 0:
            zmin = 0
        xmax = round(x+renderDistance[0])
        ymax = round(y+renderDistance[1])
        zmax = round(z+renderDistance[2])
        dims = world.dims()
        if xmax > dims[0]:
            xmax = dims[0]
        if ymax > dims[1]:
            ymax = dims[1]
        if zmax > dims[2]:
            zmax = dims[2]
        selection = world.select_data(xrange = (xmin, xmax), yrange = (ymin, ymax), zrange = (zmin, zmax))
        blocks = selection.iterate(ignore=(None,))
        glClearDepth(1.0)
        glClearColor(.5, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for bl in blocks:
            locations = bl[0]
            block = bl[1]
            cube(locations[0] - x, locations[1] - y, locations[2] - z, block)
            #print(locations[0],locations[1],locations[2])
        #location = find_pointing_direction(xrot, -yrot, 1)
        #glColor3f(1.0, 0.0, 0.0)
        #glBegin(GL_LINES)
        #print(location[0],location[1],location[2])
        #glVertex3f(0.0, 1.0, 0.0)
        #glVertex3f(0.0,0.0,1.0)
        #glVertex3f(-location[1], location[0], -location[2])
        #glEnd()

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glLineWidth(3)
        crosshair(width/2, height/2, 20)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glCullFace(GL_BACK)
        #screen.fill(currentColor)
        pygame.display.flip()
        time.sleep(.01)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mouse.set_visible(True)
                    pygame.quit()
                    return # TODO: Add pause
                else:
                    pressedKeys[event.key] = True
            if event.type == pygame.KEYUP:
                pressedKeys[event.key] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not leftClicked:
                    leftClicked = True
                    looking = get_looking_at(xrot, yrot, x, y, z, world, 10)
                    print(looking)
                    if looking != None:
                        world.set_data(looking[0],looking[1],looking[2],None)
                if event.button == 3 and not rightClicked:
                    rightClicked = True
                    looking = get_looking_at(xrot, yrot, x, y, z, world, 10)
                    print(looking)
                    if looking != None:
                        looking = list(looking)
                        if looking[3] == "n":
                            looking[2] += 1
                        elif looking[3] == "s":
                            looking[2] -= 1
                        elif looking[3] == "e":
                            looking[0] += 1
                        elif looking[3] == "w":
                            looking[0] -= 1
                        elif looking[3] == "u":
                            looking[1] += 1
                        elif looking[3] == "d":
                            looking[1] -= 1
                        try:
                            world.set_data(looking[0],looking[1],looking[2],hand)
                        except IndexError:
                            1+1
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    leftClicked = False
                if event.button == 3:
                    rightClicked = False

        xmotion = math.sin(math.radians(xrot)) * step
        zmotion = math.cos(math.radians(xrot)) * step
        if pressedKeys[K_w]:
            x += xmotion
            z -= zmotion
        if pressedKeys[K_s]:
            x -= xmotion
            z += zmotion
        if pressedKeys[K_a]:
            xmotion = math.sin(math.radians(-90+xrot)) * step
            zmotion = math.cos(math.radians(-90+xrot)) * step
            x += xmotion
            z -= zmotion
        if pressedKeys[K_d]:
            xmotion = math.sin(math.radians(xrot+90)) * step
            zmotion = math.cos(math.radians(xrot+90)) * step
            x += xmotion
            z -= zmotion
        if pressedKeys[K_SPACE]:
            y += step
        if pressedKeys[K_LSHIFT]:
            y -= step
