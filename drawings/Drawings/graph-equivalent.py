from Drawing import *

s = Drawing(alpha=0, omega=10)

# s.addColor("red", "#FF8080")
s.addNode("a")
s.addNode("b")
s.addNode("c")
s.addNode("d")
s.addNode("e")

s.addLink("a", "b", 0, 10, curving=0.1)
s.addLink("a", "c", 0, 10, curving=0.4, height=0.1)
s.addLink("b", "c", 0, 10, curving=0.1)
s.addLink("b", "d", 0, 10, curving=0.4, height=0.4)
s.addLink("c", "d", 0, 10, curving=0.1)
s.addLink("d", "e", 0, 10, curving=0.1)

# s.addRectangle("a","c",2,4,color=11)
# s.addRectangle("b","d",7,8,color="red")

s.addTimeLine(ticks=2)
