import pygame
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math


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

'''
def main(world,x,y,z,width,height,renderDistance):
    pygame.init()
    pygame.display.set_mode((width,height), DOUBLEBUF | OPENGL)
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
    gluPerspective(45, (width/height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    #glTranslatef(0.0, 0.0, -5)
    #pygame.mouse.set_visible(False)
    facing = [0, 0, False]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pygame.mouse.set_visible(True)
                    pygame.quit()
                    return # TODO: Add pause
        newMousePos = pygame.mouse.get_pos()
        change = (newMousePos[0]-(width/2), newMousePos[1]-(height/2))
        pygame.mouse.set_pos([width / 2, height / 2])
        if facing[2]:
            facing[0] -= change[0]
        else:
            facing[0] += change[0]
        facing[1] += change[1]
        while facing[0] > width:
            facing[0] = 2*width-facing[0]
            facing[2] = not facing[2]
        while facing[0] < 0:
            facing[0] = 0-facing[0]
            facing[2] = not facing[2]
        if facing[1] < 0:
            facing[1] = 0
        if facing[1] > height:
            facing[1] = height
        radius = (width**2+height**2)**.5+1
        lookingZ = (-1*facing[0]**2-facing[1]**2+radius**2)**.5
        if facing[2]:
            lookingZ *= -1
        #print(lookingZ, facing[0], facing[1], radius)
        #print(facing[0], facing[1], lookingZ)
        #glLoadIdentity()
        #gluLookAt(0, 0, 0, facing[0], facing[1], lookingZ, 0, 1, 0)
        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        glRotate(change[1]*.1,1,0,0)
        glRotate(-change[0]*.1,0,1,0)
        glMultMatrixf(modelview)
        #gluLookAt(0,0,0,8,5,6, 0, 1, 0)
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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for bl in blocks:
            locations = bl[0]
            block = bl[1]
            cube(locations[0] - x, locations[1] - y, locations[2] - z, block)
            #print(locations[0],locations[1],locations[2])
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        crosshair(width/2, height/2, 20)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glCullFace(GL_BACK)
        pygame.display.flip()
        time.sleep(.01)
'''

def main(world,x,y,z,width,height,renderDistance,step):
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
    pressedKeys = {119:False,97:False,115:False,100:False,32:False,304:False}
    while True:
        newMousePos = pygame.mouse.get_pos()
        change = (newMousePos[0]-(width/2), newMousePos[1]-(height/2))
        pygame.mouse.set_pos([width / 2, height / 2])
        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        yrot += change[1]*0.1
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
