import turtle
import random
import time

# --- Setup the Screen ---
wn = turtle.Screen()
wn.title("Cyber-Catcher: Progression Mode")
wn.bgcolor("#0a0a1a")
wn.setup(width=600, height=600)
wn.tracer(0) 

# --- Game Stats ---
score = 0
level = 1
next_level_target = 50  # Points needed to reach level 2

# --- The Player (Follows Mouse) ---
player = turtle.Turtle()
player.speed(0)
player.shape("square")
player.color("#00ffff") # Neon Cyan
player.shapesize(stretch_wid=1, stretch_len=4)
player.penup()
player.goto(0, -250)

# --- Score & Level Display ---
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

def update_ui():
    pen.clear()
    pen.write(f"Level: {level} | Score: {score} | Next Level: {next_level_target}", 
              align="center", font=("Courier", 14, "bold"))

update_ui()

# --- Game Objects ---
objects = []

def spawn_object(obj_type):
    """Creates a new object and adds it to the game."""
    obj = turtle.Turtle()
    obj.speed(0)
    
    if obj_type == "good":
        obj.shape("circle")
        obj.color("#00ff00") # Neon Green
    else:
        obj.shape("triangle")
        obj.color("#ff003c") # Neon Red
        obj.setheading(270)  # Point downwards
        
    obj.penup()
    obj.goto(random.randint(-280, 280), random.randint(300, 600))
    obj.type = obj_type
    objects.append(obj)

# Start with 3 Good Data Packets and 2 Viruses
for _ in range(3): spawn_object("good")
for _ in range(2): spawn_object("bad")

# --- Mouse Control ---
def update_mouse(event):
    mouse_x = event.x - wn.window_width() / 2
    if mouse_x < -250: mouse_x = -250
    elif mouse_x > 250: mouse_x = 250
    player.setx(mouse_x)

canvas = wn.getcanvas()
canvas.bind('<Motion>', update_mouse)

# --- Level Up Logic ---
def check_level_up():
    global level, next_level_target
    if score >= next_level_target:
        level += 1
        # Make the next level harder to reach
        next_level_target += 50 + (level * 10)
        
        # Spawn an extra Virus to make it more difficult!
        spawn_object("bad")
        
        # Flash the screen cyan to show a Level Up
        wn.bgcolor("#004444")
        wn.ontimer(lambda: wn.bgcolor("#0a0a1a"), 150)

# --- Main Game Loop ---
while True:
    wn.update()
    
    for obj in objects:
        y = obj.ycor()
        
        # Difficulty scales with your level: Objects fall faster as you progress
        base_speed = 2 if obj.type == "good" else 3
        speed_multiplier = 1 + (level * 0.15)
        obj.sety(y - (base_speed * speed_multiplier))
        
        # Reset if it falls off screen
        if obj.ycor() < -300:
            obj.goto(random.randint(-280, 280), random.randint(300, 500))
            
        # Collision detection with player
        if (obj.ycor() > -260 and obj.ycor() < -240) and (abs(obj.xcor() - player.xcor()) < 50):
            obj.goto(random.randint(-280, 280), random.randint(300, 500))
            
            if obj.type == "good":
                score += 10
            elif obj.type == "bad":
                score -= 15 # Hitting a virus hurts your progress more!
                if score < 0: score = 0
                
                # Flash the screen red on damage
                wn.bgcolor("#330000")
                wn.ontimer(lambda: wn.bgcolor("#0a0a1a"), 100)
                
            check_level_up()
            update_ui()
            
    time.sleep(0.01)