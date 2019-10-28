from Drawing import *

s = Drawing(alpha=0, omega=7)

# s.addcolor("red", "#ff8080")
s.addNode("f")
s.addNode("e")
s.addNode("d")
s.addNode("c")
s.addNode("b")
s.addNode("a")

s.addLink("b", "c", 0, 0, curving=0.1, height=0.0)
s.addLink("d", "e", 0, 0, curving=0.1, height=0.0)

# s.addLink("a", "b", 1, 1, curving=0.1, height=0.0)
s.addLink("a", "b", 1, 1, curving=0.1, height=0.0)
s.addLink("b", "c", 1, 1, curving=0.1, height=0.0)
s.addLink("c", "d", 1, 1, curving=0.1, height=0.0)
s.addLink("d", "e", 1, 1, curving=0.1, height=0.0)
s.addLink("e", "f", 1, 1, curving=0.1, height=0.0)

s.addLink("a", "b", 2, 2, curving=0.1, height=0.0)
s.addLink("c", "d", 2, 2, curving=0.1, height=0.0)
s.addLink("e", "f", 2, 2, curving=0.1, height=0.0)

s.addLink("c", "d", 3, 3, curving=0.1, height=0.0)

s.addLink("b", "c", 4, 4, curving=0.1, height=0.0)
s.addLink("c", "d", 4, 4, curving=0.1, height=0.0)
s.addLink("d", "e", 4, 4, curving=0.1, height=0.0)

s.addLink("a", "b", 5, 5, curving=0.1, height=0.0)
s.addLink("b", "c", 5, 5, curving=0.1, height=0.0)
s.addLink("d", "e", 5, 5, curving=0.1, height=0.0)
s.addLink("e", "f", 5, 5, curving=0.1, height=0.0)

# s.addRectangle("a","c",2,4,color=11)
# s.addRectangle("b","d",7,8,color="red")

s.addTimeLine(ticks=1)
