from Drawing import *

s = Drawing(alpha=0, omega=10)

# s.addColor("red", "#FF8080")
s.addNode("h")
s.addNode("g")
s.addNode("f")
s.addNode("e")
s.addNode("d")
s.addNode("c")
s.addNode("b")
s.addNode("a")

s.addLink("c", "d", 0, 0, curving=0.1, height=0.0)
s.addLink("f", "g", 0, 0, curving=0.1, height=0.0)
s.addLink("g", "h", 0, 0, curving=0.1, height=0.0)

# s.addLink("a", "b", 1, 1, curving=0.1, height=0.0)
s.addLink("c", "d", 1, 1, curving=0.1, height=0.0)
s.addLink("f", "g", 1, 1, curving=0.1, height=0.0)
s.addLink("g", "h", 1, 1, curving=0.1, height=0.0)

s.addLink("a", "b", 2, 2, curving=0.1, height=0.0)
s.addLink("b", "c", 2, 2, curving=0.1, height=0.0)
s.addLink("c", "d", 2, 2, curving=0.1, height=0.0)
s.addLink("d", "e", 2, 2, curving=0.1, height=0.0)
s.addLink("e", "f", 2, 2, curving=0.1, height=0.0)
s.addLink("f", "g", 2, 2, curving=0.1, height=0.0)
s.addLink("g", "h", 2, 2, curving=0.1, height=0.0)

s.addLink("a", "b", 3, 3, curving=0.1, height=0.0)
s.addLink("c", "d", 3, 3, curving=0.1, height=0.0)
s.addLink("e", "f", 3, 3, curving=0.1, height=0.0)

s.addLink("a", "b", 4, 4, curving=0.1, height=0.0)
s.addLink("c", "d", 4, 4, curving=0.1, height=0.0)
s.addLink("e", "f", 4, 4, curving=0.1, height=0.0)
s.addLink("g", "h", 4, 4, curving=0.1, height=0.0)

s.addLink("a", "b", 5, 5, curving=0.1, height=0.0)
s.addLink("g", "h", 5, 5, curving=0.1, height=0.0)

s.addLink("a", "b", 6, 6, curving=0.1, height=0.0)
s.addLink("c", "d", 6, 6, curving=0.1, height=0.0)
s.addLink("e", "f", 6, 6, curving=0.1, height=0.0)
s.addLink("g", "h", 6, 6, curving=0.1, height=0.0)

s.addLink("c", "d", 7, 7, curving=0.1, height=0.0)
s.addLink("e", "f", 7, 7, curving=0.1, height=0.0)
s.addLink("g", "h", 7, 7, curving=0.1, height=0.0)

s.addLink("c", "d", 8, 8, curving=0.1, height=0.0)
s.addLink("e", "f", 8, 8, curving=0.1, height=0.0)
s.addLink("g", "h", 8, 8, curving=0.1, height=0.0)

# s.addRectangle("a","c",2,4,color=11)
# s.addRectangle("b","d",7,8,color="red")

s.addTimeLine(ticks=1)
