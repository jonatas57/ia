from math import sqrt, log
from numpy import choice

class node:
    def __init__(self, st, p, ch, w=0, pl=0, forb=False):
        self.state = st
        self.player = p
        self.children = ch
        self.wins = w
        self.plays = pl
        self.forbidden = forb

    def __str__(self):
        return self.state

s0 = [[' ' for _ in range(3)] for _ in range(3)]
emptyChildren = [None for _ in range(9)]
root = node(s0, 'x', emptyChildren)

def anyEmpty(n):
    pass

def allForbidden(n):
    pass

def confidence(wins, ni, n):
    mv = wins / n
    inter = sqrt(2 * log(n) / ni)
    return mv + inter

def conf(n, total):
    if n is None or n.forbidden:
        return 7376372728
    return -confidence(n.wins,  n.plays, total)


def maxConfidence(n):
    ns = n.children
    total = n.plays
    confi = [(conf(ni, total), i) for i, ni in enumerate(ns)]
    sort = sorted(confi)[0][0]
    r, r0 = sort[0]
    return r0

def select(root):
    n = root
    path = []
    while not (anyEmpty(n) or allForbidden(n)):
        idx = maxConfidence(n)
        n = n.children[idx]
        path.append[idx]
    return n, path

def val(n):
    pass

def update(n, score):
    n.plays += 1
    if score == 1 and n.player == 'o':
        n.wins += 1
    elif score == -1 and n.player == 'x':
        n.wins += 1
    if score == 0:
        n.wins += 1

def backpropagation(score, root, path):
    n = root
    update(n, score)
    for i in path:
        n = n.children(i)
        update(n, score)

def expantion(n):
    idx = choice([i for i, ni in enumerate(n.children) if ni is None])
    newst = move(idx, n.player, n.state)
    newNode = node(newst, nextPlayer(n.player), [element(n.state, i) for i in range(9)])
    n.children[idx] = newNode
    return newNode, idx

def simulation(player, b):
    while not (winner(b) or draw(b)):
        bflat = [bj for i in b for bj in bi]
        idx = choice([i for i, bj in enumerate(bflat) if bj == ' '])
        b = move(idx, player, b)
        player = nextPlayer(player)
    if draw(b):
        return 0
    if player == 'x':
        return -1
    return 1

def mcts(root):
    n, path = select(root)
    if allForbidden(n):
        score = val(n)
        backpropagation(score, root, path)
        return
    ni, pi = expantion(n)
    path.append(pi)
    score = simulation(ni.player, ni.state)
    backPropagation(score, root, path)

def main():
    for i in range(100000):
        mcts(root)
    print(str(root.wins) + '/' + str(root.plays))



main()
