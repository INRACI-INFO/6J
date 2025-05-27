import turtle
import time

# Initialisation de Turtle
t = turtle.Turtle()
t.speed(1)  # Réglage de la vitesse de dessin

# Dessiner un cœur
t.color("red")
t.begin_fill()
t.fillcolor("red")
t.left(50)
t.forward(133)
t.circle(50, 200)
t.right(140)
t.circle(50, 200)
t.forward(133)
t.end_fill()


screen = turtle.Screen()
root = screen.getcanvas().winfo_toplevel()
root.wm_attributes("-topmost", 1) 
time.sleep(0.5) 
root.wm_attributes("-topmost", 0)  


t.hideturtle()


turtle.done()