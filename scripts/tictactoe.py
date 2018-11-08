s0 = ([[0 for i in range(3)] for j in range(3)], 0)

def jogador(s):
    t, j = s
    return j % 2 + 1

def acoes(s):
    acts = []
    t, j = s
    for i in range(len(t)):
        for j in range(len(t[i])):
            if j == 0:
                acts.append((i, j))
    return acts

def result(s, a):
    x, y = a
    t, j = s

    t[x][y] = jogador(s)
    return s

def terminal(s)

def utilidade(s, p)
