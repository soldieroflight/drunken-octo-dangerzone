import pygame
import sys
import math
from .mathutils import *

def cmp(a, b):
    return (a > b) - (a < b)

class Collider(object):
    def __init__(self,points):
        for point in points:
            assert isinstance(point,Vector2)
        self.points = points
        
    def draw(self, camera):
        camera.polygon((180,180,180), [(p.x,p.y) for p in self.points])

class RigidBody(object):
    def __init__(self, pos, ivel=Vector2(0.0), rotation=0, mass=1):
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
        self.grounded = False
        
        # External hooks. Owner should be set to the object that owns the rigid body.
        self.callback = None
        self.owner = None
        
        # various control values
        self.solid = True
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
        
def oobb_vs_oobb(box1, box2):
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
            
        # camera.circle((0,0,255), (int(colpoint.x), int(colpoint.y)), 5)
        # camera.line((255,255,0), (int(colpoint.x), int(colpoint.y)), (colpoint.x + colnormal.x*10, colpoint.y + colnormal.y*10), 4)
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

        runSimulation = box1.solid and box2.solid
        if not box1.callback is None:
            runSimulation |= box1.callback(box2)
        if not box2.callback is None:
            runSimulation |= box2.callback(box1)
            
        if runSimulation:
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
        
        if not box1.callback is None:
            box1.callback(plane)
    
    return bp
    
def oobb_vs_collider(box, collider):
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
        # camera.circle((255,255,0), (ip.x,ip.y), 6)
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
        
        if not box.callback is None:
            box.callback(collider)
        
    
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
        
        runSimulation = sphere1.solid and sphere2.solid
        if not sphere1.callback is None:
            runSimulation |= sphere1.callback(sphere2)
        if not sphere2.callback is None:
            runSimulation |= sphere2.callback(sphere1)

        if runSimulation:
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
    col = False
    
    dist = (sphere.position - plane.point) * plane.normal
    
    if dist < sphere.radius or dist < 0:
        col = True
        # Only do response if the object is solid.
        if sphere.solid:
            diff = sphere.radius - dist
            sphere.position += plane.normal.scale(diff)
            sphere.velocity = sphere.velocity.scale(-sphere.cof)
            sphere.velocity = sphere.velocity.reflect(plane.normal)
            sphere.velocity += plane.right().scale(sphere.angvel / 20.0)
            
            # angular velocity equations
            xvel = sphere.velocity * plane.right()
            sphere.angvel = xvel * plane.cof
        
        if not sphere.callback is None:
            sphere.callback(plane)
        
    return col
    
def aabb_vs_aabb(box1, box2):
    col = False
    box1xproj = box1.halfvx.project_onto(Vector2(1.0, 0.0)).mag()
    box2xproj = box2.halfvx.project_onto(Vector2(1.0, 0.0)).mag()
    
    box1yproj = box1.halfvy.project_onto(Vector2(0.0, 1.0)).mag()
    box2yproj = box2.halfvy.project_onto(Vector2(0.0, 1.0)).mag()
    
    centerdistx = math.fabs(box1.position.x - box2.position.x)
    centerdisty = math.fabs(box1.position.y - box2.position.y)
    
    if ((box1xproj + box2xproj) > centerdistx) and ((box1yproj + box2yproj) > centerdisty):
        col = True
        xdiff = max((box1xproj + box2xproj) - centerdistx, 0)
        ydiff = max((box1yproj + box2yproj) - centerdisty, 0)
            
        runSimulation = box1.solid and box2.solid
        if not box1.callback is None:
            runSimulation |= box1.callback(box2)
        if not box2.callback is None:
            runSimulation |= box2.callback(box1)

        if runSimulation:
            if not box1.useDynamics:
                pass # TODO: Box1 is a fixture.
            elif not box2.useDynamics:
                if xdiff < ydiff:
                    if (box1.position.x < box2.position.x): xdiff *= -1.0
                    box1.position.x += xdiff
                    box1.velocity.x = 0
                else:
                    applyImpulse = True
                    if (box1.position.y < box2.position.y):
                        ydiff *= -1.0
                        box1.grounded = True
                        # Travelling upwards, don't stop.
                        if (box1.velocity.y < 0):
                            applyImpulse = False
                            box1.grounded = False
                    box1.position.y += ydiff
                    if (applyImpulse):
                        box1.velocity.y = 0
            else:
                pass # TODO: Both are dynamic
                
    return col
    
def aabb_vs_plane(box, plane):
    col = False
    dist = (box.position - plane.point).project_onto(plane.normal).mag()
    ra = box.halfvx.project_onto(plane.normal).mag() + box.halfvy.project_onto(plane.normal).mag()
    bp = ra > dist
    diff = ra - dist
    
    # if isinstance(box,Player):
    if bp:
        col = True
        # Only do response if the box is solid.
        if box.solid:
            box.position += plane.normal.scale(diff)
            box.velocity -= box.velocity.project_onto(plane.normal)
            
            if plane.normal.y < -0.5: # testing against a ground plane, do grounded checks
                box.grounded = True
            
        if not box.callback is None:
            box.callback(plane)
    elif plane.normal.y < -0.5:
        box.grounded = False
    # if math.fabs(diff) < 1 and plane.normal.y < -0.5:
        # box.grounded = True
    # elif bp:
        # box.position -= plane.normal.scale(diff)
        # box.velocity = box.velocity.scale(-box.cof)
        # box.velocity = box.velocity.reflect(plane.normal)
        # colnormal = plane.normal
        # box.velocity += colnormal.scale(box.velocity.scale(0.2).mag()).project_onto(plane.right())
        
        # colnormal = plane.normal
        # rp = (corners[0] - box.position).normal()
        # denom1 = colnormal * colnormal.scale(1/box.mass)
        # denom2 = (rp.cross(colnormal))**2
        # denom = denom1 + denom2
        # if denom == 0: return bp
        # impulse = -((rpvel.scale(1 + 0.2).cross(colnormal)) / denom)
        
        # box.velocity += colnormal.scale(box.velocity.scale(0.2).mag()).project_onto(plane.right())
        
    return col
    
def aabb_vs_sphere(box, sphere):
    return False # TODO
    
def oobb_vs_sphere(box, sphere):
    return False # TODO