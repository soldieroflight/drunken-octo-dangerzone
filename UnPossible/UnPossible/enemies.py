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
DEFAULT_PATROLLING_ENEMY_WAIT_AT_POINT_TIME = 3.0

class BaseEnemy( PhysicalObject ):
    def __init__( self, pos = Vector2( 0, 0 ) ):
        super().__init__( pos )
        
        self.rigidbody = AABB( pos, DEFAULT_ENEMY_WIDTH, DEFAULT_ENEMY_HEIGHT )
        self.rigidbody.callback = self.on_collision
        
        self.state = IDLE
        self.speed = DEFAULT_ENEMY_SPEED
        self.maxHP = DEFAULT_ENEMY_HP
        self.damage = 0
        
    def update( self, deltaTime ):
        dt = self.scaleTime( deltaTime )
    
        if self.damage >= self.maxHP:
            self.setState( DEAD )
            
        self.rigidbody.update( dt )
        
    def scaleTime( self, deltaTime ):
        return deltaTime * self.timeScale
        
    def move( self, movementVector ):
        self.transform.translate( movementVector )
        self.rigidbody.position = self.transform.get_translation()
        self.rigidbody.clear_forces()
        
    def on_collision( self, other ):
        pass
        
    def debug_draw( self, camera ):
        self.rigidbody.draw( camera )
                
        
class PatrollingEnemy( BaseEnemy ):
    def __init__( self, pos = Vector2( 0, 0 ), patrolPoints = [ Vector2( 0, 0 ) ] ):
        super().__init__( pos )
        self.patrolPoints = patrolPoints
        self.curPatrolPointIdx = 0
        self.timeToWaitAtPoint = DEFAULT_PATROLLING_ENEMY_WAIT_AT_POINT_TIME
        self.waitTimer = 0.0
        
    def update( self, deltaTime ):
        super().update( deltaTime )
        
        dt = self.scaleTime( deltaTime )
        
        if self.state == IDLE:
            self.patrol( dt )
        
    def patrol( self, dt ):
        if self.rigidbody.position.approximately( self.patrolPoints[ self.curPatrolPointIdx ] ):
            self.waitTimer += dt
            if self.waitTimer >= self.timeToWaitAtPoint:
                self.waitTimer = 0
                self.curPatrolPointIdx = ( self.curPatrolPointIdx + 1 ) % len( self.patrolPoints )
            return;
            
        targetPos = self.patrolPoints[ self.curPatrolPointIdx ]
        movementVector = self.rigidbody.position - targetPos
        movementVector.normalize()
        movementVector.scale( self.speed * dt )
        self.move( movementVector )
            
            
        