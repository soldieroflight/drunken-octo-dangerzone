from baseobjects import *
from game import *

MAX_HP = 3
INVINCIBILITY_AFTER_HIT_TIME = 0.5

class Player(PhysicalObject):
    def __init__(self, game, pos=Vector2(0,0)):
        super().__init__(pos)
        self.game = game
        self.keyListener = keyboard.keyboard
        self.rigidbody = AABB(pos, 30, 60)
        self.rigidbody.owner = self
        self.speed = 180.0 # units/second
        self.jumpForce = Vector2(0.0, -35000.0)
        self.facing = 1.0
        
        self.maxHP = 5
        self.damageTaken = 0
        self.invincibilityTime = INVINCIBILITY_AFTER_HIT_TIME
        self.invincibilityTimer = self.invincibilityTime
        
        self.debugName = "Player"
        
    def update(self, deltaTime):
        super().update(deltaTime)
        
        # am i dead?
        if self.damageTaken >= self.maxHP:
            return
        
        if self.isInvincible():
            self.invincibilityTimer += deltaTime
        
        movementVector = Vector2(0.0, 0.0)
        
        self.keyListener.update()
        if (self.keyListener.get_key_just_pressed('space')) and self.rigidbody.grounded:
            self.rigidbody.add_force(self.jumpForce.scale(1.0 / 60.0 / deltaTime))
            self.rigidbody.grounded = False
        
        if not self.rigidbody.grounded:
            self.rigidbody.add_force(PLAYER_GRAVITY)
        
        # Decouple rigidbody motion from player controlled motion.
        bodyPosition = self.rigidbody.position.copy()
        # Step the player's physics.
        self.rigidbody.update(deltaTime)
        # Get the difference in rigidbody movement.
        movementVector += self.rigidbody.position - bodyPosition
        
        # Handle basic movement.
        if (self.keyListener.get_key_pressed('a') or self.keyListener.get_key_pressed('left')):
            movementVector.x -= self.speed * deltaTime
            self.facing = -1.0
        if (self.keyListener.get_key_pressed('d') or self.keyListener.get_key_pressed('right')):
            movementVector.x += self.speed * deltaTime
            self.facing = 1.0
            
        self.transform.translate(movementVector)
        
        # Synchronize the rigidbody.
        self.rigidbody.position = self.transform.get_translation()
        self.rigidbody.clear_forces()
        
        # Handle firing of projectiles.
        if (self.keyListener.get_key_just_pressed('f')):
            proj = Projectile(self.transform.get_translation().copy(), Vector2(self.facing, 0.0))
            self.game.projectiles.append(proj)
         
    def isInvincible( self ):
        return self.invincibilityTimer < self.invincibilityTime
        
    def hurt( self, damage ):
        self.damageTaken += damage
        self.invincibilityTimer = 0.0
        if self.damageTaken >= self.maxHP:
            self.debug_say( "OW I AM DEAD" )
         
    def debug_draw(self, camera):
        if self.isInvincible():
            self.rigidbody.draw(camera, (255,0,0))
        else:
            self.rigidbody.draw(camera)
        