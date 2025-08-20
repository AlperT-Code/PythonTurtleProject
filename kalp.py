import turtle

# Turtle'ı ayarla
kalp = turtle.Turtle()
kalp.shape("turtle")
kalp.color("red")
kalp.speed(10)
kalp.fillcolor("red")
kalp.begin_fill()

# Kalp şeklini çiz
kalp.left(50)
kalp.forward(133)
kalp.circle(50, 200)
kalp.right(140)
kalp.circle(50, 200)
kalp.forward(133)

# Kalbi doldur
kalp.end_fill()

# Kalbin içine yazı yaz
kalp.penup()
kalp.goto(0, 70)
kalp.pendown()
kalp.color("white")

# Turtle'ı gizle
kalp.hideturtle()

# Ekranı açık tut
turtle.done()