import math

def fitness(ax, bx, ay, by):
    d = math.sqrt((ax-bx)**2 + (ay-by)**2)
    return d

def getNeighbors(bestCandidate):
    neighbors = []
    return neighbors
    pass

if __name__ == '__main__':
    pass
x = [60, 180, 100, 140, 20]
y = [200, 200, 180, 180, 160]
pocet_miest = 5
tabuList = []
sBest = [(x[0], y[0])]
bestCandidate = [(x[0], y[0])]
tabuList.append((x[0], y[0]))
while True:
    sNeighbors = getNeighbors(bestCandidate)



