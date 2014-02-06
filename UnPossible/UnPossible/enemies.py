from baseobjects import *
from player import *

# enemy states
IDLE = 0
ATTACKING = 1
DEAD = 2

DEFAULT_ENEMY_WIDTH = 40
DEFAULT_ENEMY_HEIGHT = 40
DEFAULT_ENEMY_SPEED = 100.0
DEFAULT_ENEMY_HP = 3
DEFAULT_ENEMY_COLLISION_DAMAGE = 1
DEFAULT_PATROLLING_ENEMY_WAIT_AT_POINT_TIME = 1.0
DEBUG_DRAW_HURT_FRAMES = 10

class BaseEnemy( PhysicalObject ):
    def __init__( self, pos = Vector2( 0, 0 ) ):
        super().__init__( pos )
        
        self.rigidbody = AABB( pos, DEFAULT_ENEMY_WIDTH, DEFAULT_ENEMY_HEIGHT )
        self.rigidbody.callback = self.on_collision
        self.rigidbody.owner = self
        
        self.state = IDLE
        self.expired = False
        self.speed = DEFAULT_ENEMY_SPEED
        self.maxHP = DEFAULT_ENEMY_HP
        self.damageTaken = 0
        self.collisionDamageDone = DEFAULT_ENEMY_COLLISION_DAMAGE
        
        self.debugName = "BaseEnemy"
        self.debugDrawHurtColor = DEBUG_DRAW_HURT_FRAMES
        
    def update( self, deltaTime ):
    
        if self.state == DEAD:
            return
    
        if self.damageTaken >= self.maxHP:
            self.state = DEAD
            self.expired = True
            self.debug_say( "aiee!" )
        
        self.rigidbody.update( deltaTime )
        
        self.rigidbody.clear_forces()
        
    def move( self, movementVector ):
        self.transform.translate( movementVector )
        self.rigidbody.position = self.transform.get_translation()
        self.rigidbody.clear_forces()
        
    def on_collision( self, other ):
        if self.state == DEAD:
            return False
        if isinstance( other.owner, Player ):
            player = other.owner
            if player.isInvincible():
                return True
            player.hurt( self.collisionDamageDone )
        elif isinstance( other.owner, Projectile ):
            self.hurt( other.owner.damageDone )
        return True
        
    def hurt( self, damage ):
        if damage == 0:
            return
        self.damageTaken += damage
        self.debugDrawHurtColor = 0
        
    def debug_draw( self, camera ):
        if self.debugDrawHurtColor < DEBUG_DRAW_HURT_FRAMES or self.state == DEAD:
            self.rigidbody.draw( camera, (0, 0, 255) )
            self.debugDrawHurtColor += 1
        else:
            self.rigidbody.draw( camera )
                
        
class PatrollingEnemy( BaseEnemy ):
    def __init__( self, pos = Vector2( 0, 0 ), patrolPoints = [ Vector2( 0, 0 ) ] ):
        super().__init__( pos )
        self.patrolPoints = patrolPoints
        self.curPatrolPointIdx = 0
        self.timeToWaitAtPoint = DEFAULT_PATROLLING_ENEMY_WAIT_AT_POINT_TIME
        self.waitTimer = 0.0
        
        self.debugName = "PatrollingEnemy"
        
    def update( self, deltaTime ):
        super().update( deltaTime )
        
        if self.state == DEAD:
            return
        
        elif self.state == IDLE:
            self.patrol( deltaTime )
        
    def patrol( self, deltaTime ):
        if self.rigidbody.position.approximately( self.patrolPoints[ self.curPatrolPointIdx ] ):
            self.waitTimer += deltaTime
            if self.waitTimer >= self.timeToWaitAtPoint:
                self.waitTimer = 0
                self.curPatrolPointIdx = ( self.curPatrolPointIdx + 1 ) % len( self.patrolPoints )
            return;
            
        targetPos = self.patrolPoints[ self.curPatrolPointIdx ]
        movementVector = targetPos - self.rigidbody.position
        distanceToTarget = movementVector.mag()
        distanceToMove = min( self.speed * deltaTime, distanceToTarget )
        movementVector.normalize()
        movementVector = movementVector.scale( distanceToMove )
        self.move( movementVector )
            
            
        