def cspCreator(x, y, Cx, Cy):
    s = [[' ' for _ in range(x)] for _ in range(y)]
    X = [(i, j) for i in range(x) for j in range(y)]
    D = {pos:[True, False] for pos in X}
    C = [Cx, Cy]
    csp = (C, X, D)
    return s, csp

def cspResolver(s, csp):
    C, X, D = csp
    

    #s = [['■' for i in j] for j in s]
    return s

def prints(s):
    l = len(s[0])
    print('_' * (l+2))
    for i in s:
        print('|', end='')
        for j in i:
            print(j, end='')
        print('|')
    print('_' * (l+2))


def main():
    x = 6
    y = 3

    s, csp = cspCreator(x, y, [(x) for i in range(x)], [(y) for i in range(y)])
    #prints(cspResolver(s, csp))
    prints(s)

main()
