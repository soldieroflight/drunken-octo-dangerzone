import pygame
import math, os, sys
from mathutils import *
from collisionutils import *

pygame.init()

# global variables
FONT_SIZE = 20
LINE_WIDTH = 3
XLINEY = 460
YLINEX = 620

# set up pygame stuff
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()

# initialize the bounding boxes and their rectangle counterparts (for drawing)
box1 = AABB(Vector2(100,100),100,100)
box2 = AABB(Vector2(400,400),50,100)
boxrect1 = pygame.Rect(0,0,box1.halfvx.x*2,box1.halfvy.y*2)
boxrect2 = pygame.Rect(0,0,box2.halfvx.x*2,box2.halfvy.y*2)

# the projection axes
axisx = Vector2(x=1)
axisy = Vector2(y=1)

# collision notification
notification = pygame.font.Font(None,FONT_SIZE)

# for control
grabbed_box = None

while True:
    # pygame stuff
    clock.tick(30)
    screen.fill((0,0,0))
    
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousex, mousey = pygame.mouse.get_pos()
                point = Vector2(mousex,mousey)
                if box1.contains(point): grabbed_box = box1
                elif box2.contains(point): grabbed_box = box2
                if not grabbed_box is None: mousex,mousey = pygame.mouse.get_rel()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                grabbed_box = None
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                
    # update a box if it's being dragged
    if not grabbed_box is None:
        deltax, deltay = pygame.mouse.get_rel()
        grabbed_box.center.x += deltax
        grabbed_box.center.y += deltay
        
    # draw the two boxes
    boxrect1.center = (box1.center.x,box1.center.y)
    boxrect2.center = (box2.center.x,box2.center.y)
    pygame.draw.rect(screen,(0,0,255),boxrect1,LINE_WIDTH)
    pygame.draw.rect(screen,(0,255,0),boxrect2,LINE_WIDTH)
    
    # ####################################################################################
    # collision checks and visual debug
    box1xproj = box1.halfvx.project_onto(axisx).mag()
    box2xproj = box2.halfvx.project_onto(axisx).mag()
    
    box1yproj = box1.halfvy.project_onto(axisy).mag()
    box2yproj = box2.halfvy.project_onto(axisy).mag()
    
    centerdistx = math.fabs(box1.center.x - box2.center.x)
    centerdisty = math.fabs(box1.center.y - box2.center.y)
    
    # x-axis projections
    if (box1.center.x < box2.center.x):
        pygame.draw.line(screen,(0,0,255),(box1.center.x,XLINEY-5),(box1.center.x+box1xproj,XLINEY-5),LINE_WIDTH)
        pygame.draw.line(screen,(0,255,0),(box2.center.x,XLINEY),(box2.center.x-box2xproj,XLINEY),LINE_WIDTH)
    else:
        pygame.draw.line(screen,(0,0,255),(box1.center.x,XLINEY-5),(box1.center.x-box1xproj,XLINEY-5),LINE_WIDTH)
        pygame.draw.line(screen,(0,255,0),(box2.center.x,XLINEY),(box2.center.x+box2xproj,XLINEY),LINE_WIDTH)
    pygame.draw.line(screen,(255,0,0),(box1.center.x,XLINEY+5),(box2.center.x,XLINEY+5),LINE_WIDTH)
    
    # y-axis projection
    if (box1.center.y < box2.center.y):
        pygame.draw.line(screen,(0,0,255),(YLINEX-5,box1.center.y),(YLINEX-5,box1.center.y+box1yproj),LINE_WIDTH)
        pygame.draw.line(screen,(0,255,0),(YLINEX,box2.center.y),(YLINEX,box2.center.y-box2yproj),LINE_WIDTH)
    else:
        pygame.draw.line(screen,(0,0,255),(YLINEX-5,box1.center.y),(YLINEX-5,box1.center.y-box1yproj),LINE_WIDTH)
        pygame.draw.line(screen,(0,255,0),(YLINEX,box2.center.y),(YLINEX,box2.center.y+box2yproj),LINE_WIDTH)
    pygame.draw.line(screen,(255,0,0),(YLINEX+5,box1.center.y),(YLINEX+5,box2.center.y),LINE_WIDTH)
    
    if ((box1xproj + box2xproj) > centerdistx) and ((box1yproj + box2yproj) > centerdisty):
        text = notification.render("Collision",1,(255,255,255))
        textrect = text.get_rect()
        textrect.center = (600,465)
        screen.blit(text,textrect)
    # ####################################################################################
    
    pygame.display.update()