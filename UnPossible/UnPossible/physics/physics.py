import pygame
import sys
import math
from mathutils import *

def cmp(a, b):
    return (a > b) - (a < b)

class Collider(object):
    def __init__(self,points):
        for point in points:
            assert isinstance(point,Vector2)
        self.points = points
        
    def draw(self,screen):
        pygame.draw.polygon(screen, (180,180,180), [(p.x,p.y) for p in self.points])

class RigidBody(object):
    def __init__(self, pos, ivel, rotation=0, mass=1):
        assert isinstance(pos,Vector2)
        assert isinstance(ivel,Vector2)
        
        # various physics values
        self.position = pos
        self.rotation = rotation
        self.velocity = ivel
        self.forces = []
        self.backForces = []
        self.acceleration = Vector2(0.0,0.0)
        self.mass = mass
        self.torque = 0.0
        self.backTorque = 0.0
        self.angvel = 0.0
        self.cof = 0.7
        
        # various control values
        self.useRotation = True
        self.useDynamics = True
        self.useGravity = True
        
    def accel(self):
        facc = Vector2(0.0,0.0)
        for force in self.forces:
            facc += force
        return (facc.x,facc.y)
        
    def rotate(self,r):
        self.rotation = (self.rotation + r) % 360
        # self.set_rotation(self.rotation)
        
    def set_rotation(self,r):
        self.rotation = (r % 180) - 180
        
    def sum_forces(self):
        sum = Vector2(0.0,0.0)
        for force in self.forces:
            sum += force
        return sum
        
    def add_force(self,force):
        assert isinstance(force,Vector2)
        self.forces.append(force)
        
    def clear_forces(self):
        self.forces = []
        self.acceleration = Vector2(0.0,0.0)
        
    def add_torque(self,t):
        self.torque += t
        
    def clear_torque(self):
        self.torque = 0.0
        
    def update(self, dt):
        for force in self.backForces:
            self.add_force(force)
        self.backForces = []
        
        self.torque += self.backTorque
        self.backTorque = 0.0
        
        if self.useDynamics:
            # position using 4th order runge-kutta numerical integration
            xx1,xy1 = (self.position.x,self.position.y)
            vx1,vy1 = (self.velocity.x,self.velocity.y)
            ax1,ay1 = self.accel()
            
            xx2,xy2 = (self.position.x + 0.5*vx1*dt, self.position.y + 0.5*vy1*dt)
            vx2,vy2 = (self.velocity.x + 0.5*ax1*dt, self.velocity.y + 0.5*ay1*dt)
            ax2,ay2 = self.accel()
            
            xx3,xy3 = (self.position.x + 0.5*vx2*dt, self.position.y + 0.5*vy2*dt)
            vx3,vy3 = (self.velocity.x + 0.5*ax2*dt, self.velocity.y + 0.5*ay2*dt)
            ax3,ay3 = self.accel()
            
            xx4,xy4 = (self.position.x + vx3*dt, self.position.y + vy3*dt)
            vx4,vy4 = (self.velocity.x + ax3*dt, self.velocity.y + ay3*dt)
            ax4,ay4 = self.accel()
            
            self.position.x += (dt/6.0)*(vx1 + 2*vx2 + 2*vx3 + vx4)
            self.position.y += (dt/6.0)*(vy1 + 2*vy2 + 2*vy3 + vy4)
            self.velocity.x += (dt/6.0)*(ax1 + 2*ax2 + 2*ax3 + ax4)
            self.velocity.y += (dt/6.0)*(ay1 + 2*ay2 + 2*ay3 + ay4)
            # ###########################################################
            
            if self.useRotation:
                # angular calculations
                # self.rotation = self.rotation + self.angvel*dt
                self.rotate(self.angvel*dt)
                self.angvel = self.angvel + self.torque*dt
                self.angvel *= 0.99
        
class AABB(RigidBody):
    def __init__(self,position=None,width=0.0,height=0.0):
        assert (position is None) or isinstance(position,Vector2)
        super(AABB, self).__init__(position,Vector2(0.0,0.0),0.0)
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
        # print angle
        
        if (angle >= 315 or angle <= 45):
            return self.up
        elif (angle > 45 and angle <= 135):
            return self.right
        elif (angle > 135 and angle <= 225):
            return self.up.scale(-1.0)
        else:
            return self.right.scale(-1.0)
        
    def compute_axes(self):
        self.rotation = (self.rotation % 180) - 180
        up = Vector2(y=-1.0)
        right = Vector2(x=1.0)
        rotM = Matrix2D()
        rotM.rotate(self.rotation)
        
        self.up = rotM * up
        self.right = rotM * right
        
        vup = self.up.scale(self.halfh)
        vright = self.right.scale(self.halfw)
        
        self.topleft = self.position - vright + vup
        self.botleft = self.position - vright - vup
        self.topright = self.position + vright + vup
        self.botright = self.position + vright - vup
        
    def draw(self,screen):
        points = []
        points.append((self.topleft.x, self.topleft.y))
        points.append((self.botleft.x, self.botleft.y))
        points.append((self.botright.x, self.botright.y))
        points.append((self.topright.x, self.topright.y))
        
        vup = self.up.scale(self.halfh)
        vright = self.right.scale(self.halfw)
        pygame.draw.lines(screen, (255,255,255), True, points, 3)
        # pygame.draw.line(screen,(255,255,255),(self.position.x,self.position.y),(self.position.x+vright.x,self.position.y+vright.y),3)
        pygame.draw.line(screen,(255,255,255),(self.position.x,self.position.y),(self.position.x+vup.x,self.position.y+vup.y),3)
        
class Plane(object):
    def __init__(self, point, normal):
        assert isinstance(point,Vector2)
        assert isinstance(normal,Vector2)
        self.point = point
        self.normal = normal
        self.cof = 0.7
        
    def __str__(self):
        return "Plane going through point (%.3f, %.3f)\n"%(self.point.x, self.point.y) + \
                "\twith normal: " + str(self.normal) + "\n"
        
    def right(self):
        rotM = Matrix2D()
        rotM.rotate(90)
        return (rotM * self.normal).normal()
        
    def draw(self,screen):
        rotM = Matrix2D()
        rotM.rotate(90.0)
        vright = rotM * self.normal
        
        start = self.point + (vright.scale(1000))
        end = self.point - (vright.scale(1000))
        pygame.draw.line(screen,(255,255,255),(start.x,start.y),(end.x,end.y),3)
        
class Sphere(RigidBody):
    def __init__(self, pos, radius=0, m=1):
        assert isinstance(pos,Vector2)
        super(Sphere, self).__init__(pos,Vector2(0.0,0.0),mass=m)
        self.radius = radius
        self.cof = 0.7
        
    def __str__(self):
        return "Sphere at position (%.3f, %.3f)\n"%(self.position.x,self.position.y) + \
                "\tRadius: %.3f\n"%self.radius
        
    def draw(self,screen):
        up = Vector2(y=-1.0)
        rotM = Matrix2D()
        rotM.rotate(self.rotation)
        up = (rotM * up).normal()
        dir = up.scale(self.radius)
        pygame.draw.circle(screen, (255,255,255), (int(self.position.x), int(self.position.y)), self.radius, 3)
        pygame.draw.line(screen, (255,255,255), (int(self.position.x), int(self.position.y)), (self.position.x + dir.x,self.position.y + dir.y), 3)
        
class Player(AABB):
    initialized = 0
    def __init__(self):
        if Player.initialized:
            # print "Second player instance is being instantiated."
            sys.exit()
        Player.initialized = 1
        AABB.__init__(self,position=Vector2(100,100),width=50,height=50)
        
        self.control = [False, False]
        self.jumpForce = Vector2(0.0,-15000.0)
        self.moveForce = Vector2(500.0,0)
        self.moveSpeed = 200.0
        
        self.grounded = False
        
    def input_update(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    # self.add_force(self.moveForce.scale(-1))
                    self.control[0] = True
                if event.key == pygame.K_d:
                    # self.add_force(self.moveForce)
                    self.control[1] = True
                if event.key == pygame.K_w and self.grounded:
                    self.add_force(self.jumpForce)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.control[0] = False
                if event.key == pygame.K_d:
                    self.control[1] = False
                    
        if self.control[0]:
            # self.add_force(self.moveForce.scale(-1))
            self.velocity.x = -self.moveSpeed
        if self.control[1]:
            # self.add_force(self.moveForce)
            self.velocity.x = self.moveSpeed
        if not (self.control[0] or self.control[1]):
            self.velocity.x = 0.0
            
    def draw(self,screen):
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(self.position.x-25,self.position.y-25,50,50))
        
        
def oobb_vs_oobb(box1, box2, screen):
    bridge = box2.position - box1.position
    # first check if either of the A's axes form a separating axis
    axis = box1.up
    ra = (box1.halfh * (box1.up.project_onto(axis).mag())) + (box1.halfw * (box1.right.project_onto(axis).mag()))
    rb = (box2.halfh * (box2.up.project_onto(axis).mag())) + (box2.halfw * (box2.right.project_onto(axis).mag()))
    dist = bridge.project_onto(axis).mag()
    sa1 = (ra + rb) < dist
    sa1diff = (ra + rb) - dist
    
    if sa1: return False
    
    axis = box1.right
    ra = (box1.halfh * (box1.up.project_onto(axis).mag())) + (box1.halfw * (box1.right.project_onto(axis).mag()))
    rb = (box2.halfh * (box2.up.project_onto(axis).mag())) + (box2.halfw * (box2.right.project_onto(axis).mag()))
    dist = bridge.project_onto(axis).mag()
    sa2 = (ra + rb) < dist
    sa2diff = (ra + rb) - dist
    
    if sa2: return False
    
    # then check if either of B's axes form a separating axis
    axis = box2.up
    ra = (box1.halfh * (box1.up.project_onto(axis).mag())) + (box1.halfw * (box1.right.project_onto(axis).mag()))
    rb = (box2.halfh * (box2.up.project_onto(axis).mag())) + (box2.halfw * (box2.right.project_onto(axis).mag()))
    dist = bridge.project_onto(axis).mag()
    sa3 = (ra + rb) < dist
    sa3diff = (ra + rb) - dist
    
    if sa3: return False
    
    axis = box2.right
    ra = (box1.halfh * (box1.up.project_onto(axis).mag())) + (box1.halfw * (box1.right.project_onto(axis).mag()))
    rb = (box2.halfh * (box2.up.project_onto(axis).mag())) + (box2.halfw * (box2.right.project_onto(axis).mag()))
    dist = bridge.project_onto(axis).mag()
    sa4 = (ra + rb) < dist
    sa4diff = (ra + rb) - dist
    
    if not sa4:
        colnormal = None
        colpoint = None
        mindiff = min([sa1diff,sa2diff,sa3diff,sa4diff])
        upsame = approximately((box1.up * box2.up),1)
        upside = approximately((box1.up * box2.up),0)
        upopp = approximately((box1.up * box2.up),-1)
        if upsame or upside or upopp:
            # face-face collision
            dir = (box2.position - box1.position).normal()
            angle = math.acos(box1.up * dir)
            colnormal = None
            if angle < math.radians(45):
                colnormal = box1.up
            elif angle > math.radians(45) and angle > math.radians(45):
                angle2 = math.acos(box1.right * dir)
                if angle2 < math.radians(45):
                    colnormal = box1.right
                else:
                    colnormal = box1.right.scale(-1)
            else:
                colnormal = box1.up.scale(-1)
                
            box1.position -= colnormal.scale(mindiff/2.0)
            box2.position += colnormal.scale(mindiff/2.0)
            
            if approximately(angle, math.radians(0)):
                colpoint = Vector2((box1.position.x + box2.position.x)/2.0,(box1.position.y + box2.position.y)/2.0)
            else:
                cornersB1 = [box2.topleft,box2.botleft,box2.topright,box2.botright]
                cornersB1.sort(key=lambda x: distance(x.x,x.y,box1.position.x,box1.position.y))
                cornersB2 = [box1.topleft,box1.botleft,box1.topright,box1.botright]
                cornersB2.sort(key=lambda x: distance(x.x,x.y,box2.position.x,box2.position.y))
                colpoint = Vector2((cornersB1[0].x+cornersB2[0].x)/2.0,(cornersB1[0].y+cornersB2[0].y)/2.0)
        else:
            corners = []
            if mindiff == sa1diff or mindiff == sa2diff:
                # compute the closest corner on box2 to box1 position
                corners = [box2.topleft,box2.botleft,box2.topright,box2.botright]
                corners.sort(key=lambda x: distance(x.x,x.y,box1.position.x,box1.position.y))
                colnormal = (box2.position - box1.position).normal()
                #
                normals = [box1.up,box1.right,box1.up.scale(-1),box1.right.scale(-1)]
                normals.sort(key=lambda x: x*colnormal)
                colnormal = normals[3]
                colpoint = corners[0]
                box1.position -= colnormal.scale(mindiff/2.0)
                box2.position += colnormal.scale(mindiff/2.0)
            else:
                # compute the closest corner on box1 to box2 position
                corners = [box1.topleft,box1.botleft,box1.topright,box1.botright]
                corners.sort(key=lambda x: distance(x.x,x.y,box2.position.x,box2.position.y))
                colnormal = (box1.position - box2.position).normal()
                #
                normals = [box2.up,box2.right,box2.up.scale(-1),box2.right.scale(-1)]
                normals.sort(key=lambda x: x*colnormal)
                colnormal = normals[3]
                colpoint = corners[0]
                box2.position -= colnormal.scale(mindiff/2.0)
                box1.position += colnormal.scale(mindiff/2.0)
            
        pygame.draw.circle(screen, (0,0,255), (int(colpoint.x), int(colpoint.y)), 5)
        pygame.draw.line(screen, (255,255,0), (int(colpoint.x), int(colpoint.y)), (colpoint.x + colnormal.x*10, colpoint.y + colnormal.y*10), 4)
        test1 = box1.velocity.project_onto(colnormal)
        test2 = box2.velocity.project_onto(colnormal)
        type = test1 * test2
        if type == -(test1.mag() * test2.mag()) and type > 0: # no collision (moving away)
            return False
            
        if approximately(type,0): # contact
            b1force = box1.sum_forces()
            b2force = box2.sum_forces()
            box1.add_force(b1force.project_onto(colnormal))
            box2.add_force(b2force.project_onto(colnormal))
            return False
            
        rap = (colpoint - box1.position).normal()
        rbp = (colpoint - box2.position).normal()
        rapvel = box1.velocity + rap.scale(box1.angvel)
        rbpvel = box2.velocity + rbp.scale(box2.angvel)
        relvel = (rapvel - rbpvel)
        denom1 = colnormal * colnormal.scale((1.0/box1.mass) + (1.0/box2.mass))
        denom2 = ((rap.cross(colnormal))**2) # / inertial tensor of A
        denom3 = ((rbp.cross(colnormal))**2) # / inertial tensor of B
        denom = denom1 + denom2 + denom3
        impulse = -((relvel.scale(1 + (box1.cof + box2.cof)/2) * colnormal) / denom)
        
        # linear velocity impulses
        box1.velocity = box1.velocity + colnormal.scale(impulse/box1.mass)
        box2.velocity = box2.velocity - colnormal.scale(impulse/box2.mass)
        
        # angular velocity impulses
        box1.angvel = box1.angvel + (rap.perpendicular() * colnormal.scale(impulse/box1.mass)) # / inertial tensor of A
        box2.angvel = box2.angvel - (rbp.perpendicular() * colnormal.scale(impulse/box2.mass)) # / inertial tensor of B
        return True
    
    return False
    
def oobb_vs_plane(box,plane):
    # for the box to the plane, project the distance to the plane's point and the box's center on
    # to the planes normal, and compare this with the projection of the box's dimentions onto the normal
    box2plane = plane.point - box.position
    ra = (box.halfh * (box.up.project_onto(plane.normal).mag())) + (box.halfw * (box.right.project_onto(plane.normal).mag()))
    dist = box2plane.project_onto(plane.normal).mag()
    bp = ra > dist
    diff = ra - dist
    
    if bp:
        box.position += plane.normal.scale(diff)
        box.velocity = box.velocity.scale(-box.cof)
        box.velocity = box.velocity.reflect(plane.normal)
        
        # if approximately(math.fabs(box.up * plane.normal),1):
            # box.angvel = 0.0
            # return bp
        
        corners = [box.topleft,box.topright,box.botright,box.botleft]
        corners.sort(key=lambda x: (plane.point - x).project_onto(plane.normal).mag())
        
        # colnormal = (box.position - corners[0]).normal()
        
        # problem right now with contact with ground
        # box will not rotate by the force of gravity, because velocity and angular velocity
        # are both approximately 0.  therefore, the angular velocity calculated is approximately 0
        colnormal = plane.normal
        # rp = (corners[0] - box.position).normal()
        rp = (box.position - corners[0]).normal()
        rpvel = box.velocity + rp.scale(box.angvel)
        denom1 = colnormal * colnormal.scale(1/box.mass)
        denom2 = (rp.cross(colnormal))**2
        denom = denom1 + denom2
        if denom == 0: return bp
        impulse = -((rpvel.scale(1 + 0.2).cross(colnormal)) / denom)
        
        box.velocity += colnormal.scale(box.velocity.scale(0.2).mag()).project_onto(plane.right())
        box.angvel = (rp * colnormal.scale(impulse/box.mass))
        
        # do this only in contact situation
        # box.backTorque += (box.position - corners[0]).project_onto(plane.right()).smag()
    
    return bp
    
def oobb_vs_collider(box, collider, screen):
    assert isinstance(box,OOBB)
    assert isinstance(collider,Collider)
    
    # print box.position
    # col = False
    # for i in range(len(collider.points)-1):
        # a = collider.points[i]
        # b = None
        # if i == len(collider.points)-1:
            # b = collider.points[0]
        # else:
            # b = collider.points[i+1]
            
        # norm = Vector2(-(b.y-a.y),(b.x-a.x))
        # plane = Plane(a,norm)
        # col = col or oobb_vs_plane(box,plane)
        
    boxPoints = [box.topleft,box.topright,box.botright,box.botleft]
    col = False
    ip = None
    r = -1
    s = -1
    planea = None
    planeb = None
    for i in range(len(boxPoints)-1):
        a = boxPoints[i]
        b = None
        if i == len(boxPoints)-1:
            b = boxPoints[0]
        else:
            b = boxPoints[i+1]
        for j in range(len(collider.points)-1):
            c = collider.points[j]
            d = None
            if j == len(collider.points):
                d = collider.points[0]
            else:
                d = collider.points[j+1]
                
            # check for the intersection point of the two line segments specified by the given endpoints
            scol = False
            
            denom = ((b.x-a.x)*(d.y-c.y) - (b.y-a.y)*(d.x-c.x))
            num1 = ((a.y-c.y)*(d.x-c.x) - (a.x-c.x)*(d.y-c.y))
            num2 = ((a.y-c.y)*(b.x-a.x) - (a.x-c.x)*(b.y-a.y))
            if approximately(denom,0):
                if approximately(num1,0):
                    if (a.x < c.x and c.x < b.x) or (a.x > c.x and c.x > b.x):
                        scol = True
                        ip = Vector2((a.x + b.x)/2.0, (a.y + b.y)/2.0)
                        planea = c
                        planeb = d
            else:
                r = num1 / float(denom)
                s = num2 / float(denom)
                
                scol = (r >= 0 and r <= 1) and (s >= 0 and s <= 1)
                if scol:
                    ip = a + (b-a).scale(r)
                    planea = c
                    planeb = d
            
            col = col or scol
            
    if not ip is None:
        pygame.draw.circle(screen, (255,255,0), (ip.x,ip.y), 6)
        norm = Vector2((planeb.y-planea.y),-(planeb.x-planea.x)).normal()
        rotM = Matrix2D()
        rotM.rotate(90)
        right = rotM * norm
        # pygame.draw.line(screen, (255,255,255), (planea.x,planea.y), (planea.x+norm.x*20,planea.y+norm.y*20), 5)
        
        box2plane = box.position - planea
        ra = (box.halfh * (box.up.project_onto(norm).mag())) + (box.halfw * (box.right.project_onto(norm).mag()))
        dist = box2plane.project_onto(norm).mag()
        diff = ra - dist
        
        box.position += norm.scale(diff)
        boxPoints.sort(lambda x,y: cmp((planea - x).project_onto(norm).mag(),
                                     (planea - y).project_onto(norm).mag()))
        
        # problem right now with contact with ground
        # box will not rotate by the force of gravity, because velocity and angular velocity
        # are both approximately 0.  therefore, the angular velocity calculated is approximately 0
        colnormal = norm
        box.velocity = box.velocity.scale(-box.cof)
        box.velocity = box.velocity.reflect(colnormal)
        # rp = (corners[0] - box.position).normal()
        rp = (box.position - ip).normal()
        rpvel = box.velocity + rp.scale(box.angvel)
        denom1 = colnormal * colnormal.scale(1/box.mass)
        denom2 = (rp.cross(colnormal))**2
        denom = denom1 + denom2
        # print rpvel.scale(1 + 0.2).cross(colnormal)
        if denom == 0: return col
        impulse = -((rpvel.scale(1 + 0.2).cross(colnormal)) / denom)
        # print impulse
        
        box.velocity += colnormal.scale(box.velocity.scale(0.2).mag()).project_onto(right)
        box.angvel = (rp * colnormal.scale(impulse/box.mass))
        
    
    return col
    
def sphere_vs_sphere(sphere1,sphere2):
    # simple check: compare the distance between the centers to the sum of the radii
    # if its less, collision
    dist = distance(sphere1.position.x,sphere1.position.y,sphere2.position.x,sphere2.position.y)
    
    if dist < sphere1.radius + sphere2.radius:
        cp = (sphere1.position + sphere2.position).scale(0.5)
        colnormal = (sphere2.position - sphere1.position).normal()
        diff = (sphere1.radius + sphere2.radius) - dist
        sphere1.position -= colnormal.scale(diff/2)
        sphere2.position -= colnormal.scale(-diff/2)
        test1 = sphere1.velocity.project_onto(colnormal)
        test2 = sphere2.velocity.project_onto(colnormal)
        type = test1 * test2
        if type == -(test1.mag() * test2.mag()) and type > 0: # no collision (moving away)
            return False
        
        # calculate and apply the impulse
        relvel = sphere1.velocity - sphere2.velocity
        denom = colnormal * colnormal.scale((1.0/sphere1.mass) + (1.0/sphere2.mass))
        impulse = - ((relvel.scale(1.0 + (sphere1.cof + sphere2.cof)/2.0) * colnormal) / denom)
        
        sphere1.velocity = sphere1.velocity + colnormal.scale(impulse/sphere1.mass)
        sphere2.velocity = sphere2.velocity - colnormal.scale(impulse/sphere2.mass)
        
        # angular velocity calculations
        # combvel = min([sphere1.angvel,sphere2.angvel])
        # sphere1.angvel = combvel
        # sphere2.angvel = combvel
        s1avel = sphere1.angvel
        s2avel = sphere2.angvel
        sphere1.angvel = ((s1avel - s2avel) * sphere1.cof) / sphere1.mass # inertial tensor of sphere 1
        sphere2.angvel = ((s2avel - s1avel) * sphere2.cof) / sphere2.mass # inertial tensor of sphere 2
        
        return True
    return False
    
def sphere_vs_plane(sphere,plane):
    # simple check here too: project the vector from the sphere to the point on the plane
    # onto the planes normal.  if the magnitude of the projection is less than the radius,
    # collision
    
    dist = (sphere.position - plane.point) * plane.normal
    
    if dist < sphere.radius or dist < 0:
        diff = sphere.radius - dist
        sphere.position += plane.normal.scale(diff)
        sphere.velocity = sphere.velocity.scale(-sphere.cof)
        sphere.velocity = sphere.velocity.reflect(plane.normal)
        sphere.velocity += plane.right().scale(sphere.angvel / 20.0)
        
        # angular velocity equations
        xvel = sphere.velocity * plane.right()
        sphere.angvel = xvel * plane.cof
        
        return True
    return False
    
def aabb_vs_plane(box, plane):
    dist = (box.position - plane.point).project_onto(plane.normal).mag()
    ra = box.halfvx.project_onto(plane.normal).mag() + box.halfvy.project_onto(plane.normal).mag()
    bp = ra > dist
    diff = ra - dist
    
    if isinstance(box,Player):
        if bp:
            box.position += plane.normal.scale(diff)
            box.velocity -= box.velocity.project_onto(plane.normal)
            
            if plane.normal.y < -0.5: # testing against a ground plane, do grounded checks
                box.grounded = True
        elif plane.normal.y < -0.5:
            box.grounded = False
        if math.fabs(diff) < 1 and plane.normal.y < -0.5:
            box.grounded = True
    elif bp:
        box.position -= plane.normal.scale(diff)
        box.velocity = box.velocity.scale(-box.cof)
        box.velocity = box.velocity.reflect(plane.normal)
        colnormal = plane.normal
        # box.velocity += colnormal.scale(box.velocity.scale(0.2).mag()).project_onto(plane.right())
        
        # colnormal = plane.normal
        # rp = (corners[0] - box.position).normal()
        # denom1 = colnormal * colnormal.scale(1/box.mass)
        # denom2 = (rp.cross(colnormal))**2
        # denom = denom1 + denom2
        # if denom == 0: return bp
        # impulse = -((rpvel.scale(1 + 0.2).cross(colnormal)) / denom)
        
        # box.velocity += colnormal.scale(box.velocity.scale(0.2).mag()).project_onto(plane.right())