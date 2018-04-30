import pygame
import math  # Function that allows vectors and trig
import random  # Function that allows random generation
import time

filePath = "C:\\Users\\jmurr\\OneDrive\\Computing\\Computer Science(1)\\Pygame\\"  # Set default path location

pygame.init()
clock = pygame.time.Clock()

displayWidth = 1300
displayHeight = 680
screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Balls")

white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 155, 0)
black = (0, 0, 0)
orange = (255, 165, 0)
purple = (75, 0, 130)
mint = (203, 255, 250)

screen.fill(mint)

font = pygame.font.SysFont(None, 70, False, False, None)
font2 = pygame.font.SysFont(None, 20, False, False, None)


def text(text, col):
    textSurf = font.render(text, True, col)
    return textSurf, textSurf.get_rect()


def text2(text, col):
    textSurf2 = font2.render(text, True, col)
    return textSurf2, textSurf2.get_rect()


def message(msg, col):
    textSurf, textRect = text(msg, col)
    textRect.center = (displayWidth/2, displayHeight / 2)
    screen.blit(textSurf, textRect)


# Define functions status that displays whether drag, elasticity. gravity or collision is on
def statusdra(msg, col):
    textSurf2, textRect2 = text2(msg, col)
    textRect2.center = (displayWidth/20, displayHeight / 20)
    screen.blit(textSurf2, textRect2)


def statuselas(msg, col):
    textSurf2, textRect2 = text2(msg, col)
    textRect2.center = (displayWidth/8, displayHeight / 20)
    screen.blit(textSurf2, textRect2)


def statusgrav(msg, col):
    textSurf2, textRect2 = text2(msg, col)
    textRect2.center = (displayWidth / 5, displayHeight / 20)
    screen.blit(textSurf2, textRect2)


def statuscol(msg, col):
    textSurf2, textRect2 = text2(msg, col)
    textRect2.center = (displayWidth / 2, displayHeight / 20)
    screen.blit(textSurf2, textRect2)


# Adds a vextor quantity to an object
def addvectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2 # Defines x using trigonometry
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2 # Defines Y using trigonometry
    angle = 0.5 * math.pi - math.atan2(y, x) # Defines angle using trig atan = arctan
    length = math.hypot(x, y) # Sets the length of the vector, hypot = hypotenuse

    return angle, length # Returns angle and length


# Collision function
def collide(ball1, ball2):
        dx = ball1.x - ball2.x  # X Distance between the balls
        dy = ball1.y - ball2.y  # Y Distance between the balls

        distance = math.hypot(dx, dy)  # Distance is the hypotenuse of the x and y
        if distance < ball1.size + ball2.size:  # If the distance is short enough to be touching

                myBalls.remove(ball2)  # Delete the ball
                if ball.size < displayHeight/2:  # If the ball left is below a certain size
                    ball.size += int(ball2.size/6)  # Increase it by the size of the deleted
                    return -1





# Puts message on screen
message('Loading?', black)

# Set original values for forces
drag = 1
dra = False
elastic = 1
elas = False
gravity = 0
grav = False
collision = False


# Creates a new class to allow the creation of balls
class ball:
    def __init__(self, x, y, s, t, sp, a, c):  # Defines balls based on size, colour etc.
        self.x = x
        self.y = y
        self.size = s
        self.colour = c
        self.thiccness = t
        self.angle = a
        self.speed = sp

    def display(self): # Function that draws the ball and a hit box around the ball
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thiccness)
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.size/2, self.size/2))

    def move(self):  # Defines the movement of a ball using trig and the add vector function
        (self.angle, self.speed) = addvectors(self.angle, self.speed, math.pi, gravity)  # Input of gravity as permenant down vector
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag  # Multiply the speed by drag to add realistic force

    def bounce(self): # Defines bouncing of the balls, if they touch the side the angle is reversed
        if self.x > displayWidth - self.size:  # X boundary
            self.x = 2 * (displayWidth - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elastic  # Every time the ball is bounced it loses energy, if elas is enabled

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elastic

        if self.y > displayHeight - self.size:  # Y boundary
            self.y = 2 * (displayHeight - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elastic

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elastic

    def update(self):  # Update function that brings together display, movement and bouncing
        ball.display()
        ball.move()
        ball.bounce()


# Sets number of starting balls
ballNumber = 1000
myBalls = []  # Creates a new list of balls
ballSprites = pygame.sprite.Group() # Sets a new sprite group for balls
ballSprites.add(myBalls)  # Adds list of balls to sprite group
for n in range(ballNumber):  # Generates balls according to ball number
    size = random.randint(5, 20) # Generates random size
    thicc = 0  # Set thiccness as 0
    x = random.randint(0, displayWidth)  # Generate random x and y calues
    y = random.randint(0, displayHeight)
    colour = (mint)
    while colour == mint:  # If the colour of the ball is the colour of the background regenerate the colour
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    speed = random.randint(5,8) # Generate random speed
    angle = random.uniform(0, math.pi * 2) # Generate random angle
    myBalls.append(ball(x, y, size, thicc, speed, angle, colour))  # Adds ball to list of balls
    pygame.display.update()  # Update display

gameExit = False
gameLoop = True

while gameLoop:
    # pygame.draw.rect(screen, green, (150, 450, 100, 50)) !!!Test code for buttons!!!
    # pygame.draw.rect(screen, red, (550, 450, 100, 50))
    # pygame.display.update()
    screen.fill(mint)  # Sets background colour as mint
    message('Loading.', black)  # Arbitrary loading screen
    time.sleep(0.5)
    pygame.display.update()
    screen.fill(mint)

    message('Loading..', black)
    time.sleep(0.5)
    pygame.display.update()
    screen.fill(mint)

    message('Loading...', black)
    time.sleep(0.5)
    pygame.display.update()
    screen.fill(mint)

    message('Loading....', black)
    time.sleep(0.5)
    pygame.display.update()

    pygame.display.update()
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Input of p and o turn gravity off and on
                    gravity = 0
                    grav = False
                    print("done ")
                if event.key == pygame.K_o:
                    gravity = 0.002
                    grav = True
                    print("done ")

                if event.key == pygame.K_l:  # Input l and k turn drag off and on
                    drag = 1
                    dra = False
                    print("done ")
                if event.key == pygame.K_k:
                    drag = 0.999
                    dra = True
                    print("done ")

                if event.key == pygame.K_m:  # Input of m and n turn elasticity off and on
                    elastic = 1
                    elas = False
                    print("done ")
                if event.key == pygame.K_n:
                    elastic = 0
                    elas = True
                    print("done ")

                if event.key == pygame.K_h:   # Input of h and g turn collision off and on
                    collision = False
                    print("done ")
                if event.key == pygame.K_g:
                    collision = True
                    print("done ")

        screen.fill(mint)  # Refill screen to prevent trails

        # List of selection statement to display status of forces on screen
        if dra:
            statusdra("drag : ON", black)
        else:
            statusdra("drag : OFF", black)

        if elas:
            statuselas("elas : ON", black)
        else:
            statuselas("elas : OFF", black)

        if grav:
            statusgrav("grav : ON", black)
        else:
            statusgrav("grav : OFF", black)

        if collision:
            statuscol("Col : ON", black)
        else:
            statuscol("Col : OFF", black)

        myBalls.sort(key=lambda x: x.size, reverse=True)

        for i, ball in enumerate(myBalls):  # Assigns number to all balls
            if collision:  # If collision is on run through all balls and check if they are touching and collide
                for ball2 in myBalls[i + 1:]:
                        collide(ball, ball2)

            ball.update()  # Updates all balls in list
        ballNumber = 0  # Sets number of balls to 0 temporarily

        #for i in myBalls (len(myBalls):
        #   if i.size > (i+1).size:


        for ball in myBalls:  # Sets the pygame caption to the number of balls on screen
            ballNumber += 1
        pygame.display.set_caption("Balls: " + str(ballNumber))

        pygame.display.update()  # Updates display
        clock.tick(60)  # Sets FPS to 60
    gameLoop = False
