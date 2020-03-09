import turtle
from datetime import datetime
turtle.penup()
turtle.fd(-300)
turtle.pnesize = 100

def drawLine(draw):   #draw 是否画下
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(50)
    turtle.right(90)

def formatTime():
    return datetime.now().strftime("%Y:%m:%d")

def drawNuber(number):
    drawLine(True)  if number in [2,3,4,5,6,8,9]  else drawLine(False)
    drawLine(True)  if number in [0,1,3,4,5,6,7,8,9]  else drawLine(False)
    drawLine(True)  if number in [0,2,3,5,6,8] else drawLine(False)
    drawLine(True)  if number in [0,2,6,8] else drawLine(False)
    turtle.left(90)
    drawLine(True)  if number in [0,4,5,6,8,9]  else drawLine(False)
    drawLine(True)  if number in [0,2,3,5,6,7,8,9]  else drawLine(False)
    drawLine(True)  if number in [0,1,2,3,4,7,8,9]  else drawLine(False)

def drawColon(colon=":"):
    turtle.color("orange")
    turtle.write(colon, font =("Times", 24, "bold"))
    turtle.penup()
    turtle.seth(0)
    turtle.fd(40)

def drawRun(n):
    count  = 0
    try:
        n  = str(n)
    except Exception as e:
        print("值错误")
        exit()
    turtle.color("blue") 
    for i in n:
        if i == ":":
            if count == 0:
                drawColon("年")
                turtle.color("green") 
            elif count == 1:
                drawColon("月")
                turtle.color("cyan")
            elif count == 2:
                drawColon("日")
            count+= 1
        else:
            i = int(i)
            drawNuber(i)
            turtle.right(180)
            turtle.penup()
            turtle.fd(20)


time = formatTime()
drawRun(time)
# drawRun(2010)
turtle.done()