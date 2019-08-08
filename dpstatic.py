import random, numpy

xMax=10
d=1
n=10

x=map(lambda x:random.randint(0,xMax-1),[0]*n)
print x
argsort=list(numpy.argsort(x))+[n]

##DEBUG
#xx=list(x)
#xx.sort()
#print xx
#print argsort
#print map(lambda i:x[i],argsort[:-1])
#nbZero=len(filter(lambda x: x==0, x))
#print nbZero

M=[0]*(n+1)
firstSeen=[True]*n
print ">> Proceeding DP for maximum matching:"
for i in range(1,n):
  if abs(x[argsort[i]]-x[argsort[i-1]])<=d:
    M[argsort[i]]=M[argsort[i-2]]+1
    if firstSeen[argsort[i]] and firstSeen[argsort[i-1]]:
      print "  ...found vertices:", argsort[i], argsort[i-1], "; x-positions:", x[argsort[i]], x[argsort[i-1]]
      firstSeen[argsort[i]]=False
      firstSeen[argsort[i-1]]=False
  else:
    M[argsort[i]]=M[argsort[i-1]]
print "--> Maximum matching size:", reduce(max,M)
  

