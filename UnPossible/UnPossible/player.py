from baseobjects import *
from game import *
from physics.particles import *
from animatedObject import *

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

        self.animation = AnimatedObject("..\Art\WidgetIdle.png", 2, 6)
        self.animation.animate(0, 5, 5, True)

        # Jetpack
        self.hasJetpack = True # For debugging...
        self.releasedSpacePostJump = False
        self.jetpackForce = PLAYER_GRAVITY.scale(-1.25)
        self.jetpackTime = 0.0
        self.maxJetpackTime = 1.5
        self.jetpackParticles = ParticleEmitter(self.rigidbody.position, {'colors': [(255, 0, 0)],
                                                                          'movementFrame': 'inherited',
                                                                          'inheritance': 0.5,
                                                                          'emitterArea': 1,
                                                                          'minEmitRate': 15,
                                                                          'maxEmitRate': 30,
                                                                          'maxSize': 5,
                                                                          'velocity': Vector2(0, 150.0),
                                                                          'randomVelocity': Vector2(10.0, 8),
                                                                          'minLifetime': 1.0,
                                                                          'maxLifetime': 3.0,
                                                                          'damping': 0.98})
        self.game.particles.append(self.jetpackParticles)
        self.jetpackParticles.pause()
        
        self.maxHP = 5000
        self.damageTaken = 0
        self.invincibilityTime = INVINCIBILITY_AFTER_HIT_TIME
        self.invincibilityTimer = self.invincibilityTime
        
        self.debugName = "Widget"
        
    def update(self, deltaTime):
        super().update(deltaTime)
        self.animation.update(deltaTime)
        
        # am i dead?
        if self.damageTaken >= self.maxHP:
            return
        
        if self.isInvincible():
            self.invincibilityTimer += deltaTime
        
        movementVector = Vector2(0.0, 0.0)
        
        self.keyListener.update()
        if (self.keyListener.get_key_just_pressed('space')) and self.rigidbody.grounded:
            self.rigidbody.add_force(self.jumpForce.scale(1.0 / 60.0 / deltaTime))

        # Jetpack
        if self.hasJetpack:
            if not self.rigidbody.grounded:
                if not self.releasedSpacePostJump:
                    if not self.keyListener.get_key_pressed('space'):
                        self.releasedSpacePostJump = True
                elif self.keyListener.get_key_pressed('space') and self.jetpackTime > 0:
                    # Activate jetpack!
                    self.jetpackParticles.unpause()
                    self.jetpackTime -= deltaTime
                    timeForForce = deltaTime
                    if self.jetpackTime <= 0.0:
                        timeForForce += self.jetpackTime # < 0, so addition lowers time
                        self.jetpackTime = 0.0
                    timeScale = (timeForForce / deltaTime)
                    self.rigidbody.add_force(self.jetpackForce.scale(timeScale))
                else:
                    self.jetpackParticles.pause()
            else:
                self.releasedSpacePostJump = False
                self.jetpackTime = self.maxJetpackTime # Instant recharge
                self.jetpackParticles.pause()
                # Recharging?
                #self.jetpackTime += deltaTime
                #if self.jetpackTime > self.maxJetpackTime:
                #    self.jetpackTime = self.maxJetpackTime
        
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
        if (self.keyListener.get_key_just_pressed('e')):
            proj = TimeProjectile(self.game, 0.2, self.transform.get_translation().copy(), Vector2(self.facing, 0.0), 100)
            self.game.projectiles.append(proj)

        self.rigidbody.grounded = False

    def sync_transform(self):
        super().sync_transform()
        self.jetpackParticles.pos = self.rigidbody.position
         
    def isInvincible( self ):
        return self.invincibilityTimer < self.invincibilityTime
        
    def hurt( self, damage ):
        self.damageTaken += damage
        self.invincibilityTimer = 0.0
        if self.damageTaken >= self.maxHP:
            self.debug_say( "OW I AM DEAD" )

    def draw(self, camera):
        self.animation.draw(camera, self.rigidbody.position, (0, -30))
        self.debug_draw(camera)
         
    def debug_draw(self, camera):
        if self.isInvincible():
            self.rigidbody.draw(camera, (255,0,0))
        else:
            self.rigidbody.draw(camera)
        
