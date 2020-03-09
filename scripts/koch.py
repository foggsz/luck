import turtle
import os
# print(os.environ["TCL_LIBRARY"])
# print(os.environ["TK_LIBRARY"])
def koch(size, n):
    if n == 0:
        turtle.fd(size)
    else:
        angles = [0, 60, -120, 60]
        for angle  in angles:
            turtle.left(angle)
            koch(size/3, n-1)
    

def main():
    turtle.setup(800,800)
    turtle.penup()
    turtle.goto(-300, 200)
    turtle.pendown()
    turtle.pensize(2)
    level = 4
    size = 500
    koch(size, level)
    turtle.right(120)
    koch(size, level)
    turtle.right(120)
    koch(size, level)

main()
turtle.done()