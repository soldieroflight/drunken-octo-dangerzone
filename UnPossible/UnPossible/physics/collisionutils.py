# ############################################################################
# collisionutils.py - Python version of the AABB, OOBB and Sphere collision
#                       classes.
#
# Author: Kevin Todisco
# ############################################################################

import pygame
from .mathutils import *
from .physics import *

class AABB(RigidBody):
    def __init__(self,center=None,width=0.0,height=0.0):
        assert (center is None) or isinstance(center,Vector2)
        super().__init__(center)
        self.halfvx = Vector2(x=width/2.0)
        self.halfvy = Vector2(y=height/2.0)
        self.useRotation = False
        
    def __str__(self):
        return "AABB at position (%.3f, %.3f) with half-vectors:\n\t"%(self.position.x,self.position.y) + \
               str(self.halfvx) + "\n\t" + \
               str(self.halfvy)
                    
    def contains(self,point):
        assert isinstance(point,Vector2)
        
        return (point.x <= (self.position.x + self.halfvx.x)) and (point.x >= (self.position.x - self.halfvx.x)) and \
               (point.y <= (self.position.y + self.halfvy.y)) and (point.y >= (self.position.y - self.halfvy.y))
               
    def draw(self, camera):
        topleft = self.position - self.halfvx - self.halfvy
        botleft = self.position - self.halfvx + self.halfvy
        topright = self.position + self.halfvx - self.halfvy
        botright = self.position + self.halfvx + self.halfvy
        
        points = []
        points.append((topleft.x, topleft.y))
        points.append((botleft.x, botleft.y))
        points.append((botright.x, botright.y))
        points.append((topright.x, topright.y))
        
        camera.lines((255,255,255), True, points, 3)
               
class OOBB(RigidBody):
    def __init__(self,center=None,width=0.0,height=0.0,rotation=0.0):
        assert isinstance(center,Vector2)
        super(OOBB, self).__init__(center,Vector2(0.0,0.0),rotation)
        self.halfw = width/2.0
        self.halfh = height/2.0
        # self.rotation = rotation
        self.up = Vector2(y=1.0)
        self.right = Vector2(x=1.0)
        
        vright = self.right.scale(self.halfw)
        vup = self.up.scale(self.halfh)
        self.topleft = self.position - vright + vup
        self.botleft = self.position - vright - vup
        self.topright = self.position + vright + vup
        self.botright = self.position + vright - vup
        
    def __str__(self):
        return "OOBB at position (%.3f, %.3f) with sizes:\n\t"%(self.position.x,self.position.y) + \
               "Width: %.3f\n\t"%float(self.halfw * 2) + \
               "Height: %.3f\n\t"%float(self.halfh * 2) + \
               "and rotated %.3f degrees\n"%float(self.rotation)
     
    def contains(self,point):
        assert isinstance(point,Vector2)
        dist = math.sqrt((self.position.x - point.x)**2 + (self.position.y - point.y)**2)
        if dist < self.halfw:
            return True
        return False
        
    def face_normal(self,point):
        assert isinstance(point,Vector2)
        v = (point - self.position)
        angle = math.degrees(math.acos((v * self.up)/(v.mag()*self.up.mag())))
        
        if (angle >= 315 or angle <= 45):
            return self.up
        elif (angle > 45 and angle <= 135):
            return self.right
        elif (angle > 135 and angle <= 225):
            return self.up.scale(-1.0)
        else:
            return self.right.scale(-1.0)
        
    def compute_axes(self):
        up = Vector2(y=-1.0)
        right = Vector2(x=1.0)
        rotM = Matrix2D()
        rotM.rotate(self.rotation)
        
        self.up = rotM * up
        self.right = rotM * right
        
    def draw(self, camera):
        vup = self.up.scale(self.halfh)
        vright = self.right.scale(self.halfw)
        
        self.topleft = self.position - vright + vup
        self.botleft = self.position - vright - vup
        self.topright = self.position + vright + vup
        self.botright = self.position + vright - vup
        
        points = []
        points.append((self.topleft.x, self.topleft.y))
        points.append((self.botleft.x, self.botleft.y))
        points.append((self.botright.x, self.botright.y))
        points.append((self.topright.x, self.topright.y))
        
        camera.lines((255,255,255), True, points, 3)
        # pygame.draw.line(screen,(255,255,255),(self.position.x,self.position.y),(self.position.x+vright.x,self.position.y+vright.y),3)
        camera.line((255,255,255),(self.position.x,self.position.y),(self.position.x+vup.x,self.position.y+vup.y),3)
        
class Plane(object):
    def __init__(self, point, normal):
        assert isinstance(point,Vector2)
        assert isinstance(normal,Vector2)
        self.point = point
        self.normal = normal
        self.cof = 0.4
        
    def __str__(self):
        return "Plane going through point (%.3f, %.3f)\n"%(self.point.x, self.point.y) + \
                "\twith normal: " + str(self.normal) + "\n"
        
    def right(self):
        rotM = Matrix2D()
        rotM.rotate(90)
        return (rotM * self.normal).normal()
        
    def draw(self, camera):
        rotM = Matrix2D()
        rotM.rotate(90.0)
        vright = rotM * self.normal
        
        start = self.point + (vright.scale(1000))
        end = self.point - (vright.scale(1000))
        camera.line((255,255,255),(start.x,start.y),(end.x,end.y),3)
        
class Sphere(RigidBody):
    def __init__(self, pos, radius=0, m=1):
        assert isinstance(pos,Vector2)
        super(Sphere, self).__init__(pos,Vector2(0.0,0.0),mass=m)
        self.radius = radius
        self.cof = 0.7
        
    def __str__(self):
        return "Sphere at position (%.3f, %.3f)\n"%(self.position.x,self.position.y) + \
                "\tRadius: %.3f\n"%self.radius
        
    def draw(self, camera):
        up = Vector2(y=-1.0)
        rotM = Matrix2D()
        rotM.rotate(self.rotation)
        up = (rotM * up).normal()
        dir = up.scale(self.radius)
        camera.circle(screen, (255,255,255), (self.position.x,self.position.y), self.radius, 3)
        camera.line(screen, (255,255,255), (self.position.x,self.position.y), (self.position.x + dir.x,self.position.y + dir.y), 3)
        