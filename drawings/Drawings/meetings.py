from Drawing import *

s = Drawing(alpha=0, omega=24)

#s.addColor("red", "#FF8080")
s.addNode("a",[(0,8), (12,24)])
s.addNode("b",[(0,8), (12,18)])
s.addNode("c")
s.addNode("d",[(5,24)])
s.addNode("e")
s.addNode("f")

s.addLink("a","b",4,8,curving=0.1)
s.addLink("a","b",12,16,curving=0.1)
s.addLink("a","c",2,6,height=0.4,curving=0.2)
s.addLink("a","c",18,20,height=0.4,curving=0.2)
s.addLink("b","c",4,6,curving=0.1)
s.addLink("c","d",10,12,curving=0.1)
s.addLink("c","d",22,24,curving=0.1)
s.addLink("c","e",8,10,height=0.4,curving=0.2)
s.addLink("c","e",12,14,height=0.4,curving=0.2)
s.addLink("d","e",6,8,curving=0.1)
s.addLink("d","e",20,22,curving=0.1)
s.addLink("d","f",12,22,height=0.4,curving=0.2)
s.addLink("e","f",0,4,curving=0.1)
s.addLink("e","f",10,12,curving=0.1)
s.addLink("e","f",20,24,curving=0.1)

#s.addRectangle("a","c",2,4,color=11)
#s.addRectangle("b","d",7,8,color="red")

s.addTimeLine(ticks=2)

