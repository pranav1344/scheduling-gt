import random
import time
import csv

class UndirectedGraph:
    def __init__(self):
        self.colors = []
        self.vertices = {}
    def add_vertex(self, vertex):
        self.colors.append(vertex.color)
        self.vertices[vertex.label] = vertex
    def add_edge(self, vertex1, vertex2):
        self.vertices[vertex1].add_neighbor(self.vertices[vertex2])
        self.vertices[vertex2].add_neighbor(self.vertices[vertex1])
    def add_vertex(self, label, weight):
        self.vertices[label] = vertex(label, weight)
    def print(self):
        for i in self.vertices.keys():
            for j in self.vertices[i].neighors:
                print("Edge from " + str(i) + " -- " + str(j.label))
                print("Colors are " + str(self.vertices[i].color) + " -- " + str(j.color))


class vertex:
    def __init__(self, label, weight, color):
        self.label = label
        self.weight = weight
        self.color = 0
        self.neighors = set()
    def __init__(self, label, weight):
        self.label = label
        self.weight = weight
        self.color = 0
        self.neighors = set()
    def add_neighbor(self, vertex):
        if vertex not in self.neighors:
            self.neighors.add(vertex)




def BruteForceColorGraph(g, iter = -1):
    if iter == -1:
        iter = len(g.vertices.keys())
    t1 = time.time()
    for j in range(iter):
        if (time.time() - t1) > 150:
            return
        for i in g.vertices.values():
            i.color = 0
        if colorGraph(g, 0, j + 1):
            return
        

def printColors(g):
    for i in g.vertices.values():
        print(i.color, end= ' ')
    print()

def colorsUserd(g):
    colors = set()
    for i in g.vertices.values():
        colors.add(i.color)
    return len(colors)


def isColorValid(g):
    for i in g.vertices.values():
        for j in i.neighors:
            if i.color == j.color:
                return False
    return True
def colorGraph(g, i, colors):
    if i >= len(g.vertices.keys()):
        if isColorValid(g):
            return True
        return False
    for j in range(1, colors + 1):
        g.vertices[i].color = j
        if colorGraph(g , i + 1, colors):
            return True
        g.vertices[i].color = 0
    return False

    

def MakeMove(i, g, colors):
    attempt = False
    current_payoff = colors[i.color]
    for k in colors.keys():
        if i.color != k and colors[k] + i.weight > current_payoff:
            conflict = False
            for j in i.neighors:
                if(k == j.color):
                    conflict = True
                    break
            if conflict != True:
                temp = i.color
                i.color = k
                colors[k] += i.weight
                attempt = True
                colors[temp] -= i.weight
    return attempt


def GameTheoryColoring(g):
    colors = {}
    for i in g.vertices.values():
        i.color = i.label + 1
        colors[i.color] = i.weight
    movesPossible = True
    iter = 0
    while movesPossible:
        iter+=1
        for i in g.vertices.values():
            if MakeMove(i, g, colors):
                movesPossible = True
            else:
                movesPossible = False

# test_cases = [(i + 1) for i in range(10)]
# for j in test_cases:
#     g = UndirectedGraph()
#     for i in range(j):
#         g.add_vertex(i, random.randint(0, 100))

#     for i in range(j):
#         for j in range(j):
#             if random.random() >= 0.5 and i != j:
#                 g.add_edge(i, j)
#     print("Vertices : " + str(len(g.vertices.values())))
#     brute_t1 = time.time()
#     BruteForceColorGraph(g)
#     brute_t2 = time.time()
#     colorsUserd(g)
#     print("Time taken by brute force :" + str(brute_t2 - brute_t1))
#     # printColors(g)
#     # g.print()
#     game_theory_t1 = time.time()
#     GameTheoryColoring(g)
#     game_theory_t2 = time.time()
#     # printColors(g)
#     # g.print()
#     colorsUserd(g)
#     print("Time taken by algorithm :" + str(game_theory_t2 - game_theory_t1))
#     print('-' * 50)

def checkInterference(i, start, end):
    start_1 = i["start"]
    end_1 = i["end"]
    if start < end_1 and end > start_1:
        return True
    return False

f = open('stats.txt', mode='+a')

with open('stats.csv', mode='+a') as csvfile:
    for i in range(10000):
        csvwriter = csv.writer(csvfile)
        alertGraph = UndirectedGraph()
        alerts = {}
        def add_alert(label, start, end, weight):
            alert = {}
            alert["start"] = start
            alert["end"] = end
            alert["label"] = label
            alerts[label] = alert
            alertGraph.add_vertex(label=label, weight=weight)
            for i in alerts.values():
                if i["label"] != label and checkInterference(i, start, end):
                    alertGraph.add_edge(label, i["label"])

        alert_list_size = random.randint(4, 15)
        for i in range(alert_list_size):
            start = random.randint(0,1000)
            end = random.randint(start + 1, 1001)
            weight = random.random() * 100
            label = i
            add_alert(label=label, start=start, end=end, weight=weight)

        print(alerts)
        game_theory_t1 = time.time()
        GameTheoryColoring(alertGraph)
        game_theory_t2 = time.time()
        # printColors(g)
        # g.print()
        print("Time taken by algorithm :" + str(game_theory_t2 - game_theory_t1))
        print('-' * 50)
        f.write('\n')
        f.write('Alerts : ' + str(len(alertGraph.vertices.keys())))
        f.write('\n')
        f.write("Time taken by algorithm :" + str(game_theory_t2 - game_theory_t1))
        f.write('\n')
        f.write("Colors used by algorithm : " + str(colorsUserd(alertGraph)))
        gtcolors = str(colorsUserd(alertGraph))
        f.write('\n')
        brute_t1 = time.time()
        BruteForceColorGraph(alertGraph)
        brute_t2 = time.time()
        brutefcolors = str(colorsUserd(alertGraph))
        print("Time taken by brute force : " + str(brute_t2 - brute_t1))
        f.write('\n')
        f.write("Time taken by brute force :" + str(brute_t2 - brute_t1))
        f.write('\n')
        f.write("Colors used by brute force : " + str(colorsUserd(alertGraph)))
        csvwriter.writerow([str(len(alertGraph.vertices.keys())), str(game_theory_t2 - game_theory_t1), gtcolors, str(brute_t2 - brute_t1), brutefcolors])
        f.write('\n')
        print('-' * 50)

        # printColors(g)
        # g.print()



