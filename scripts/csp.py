def Revise(csp, i, j):
    X, D, C = csp
    violate = set([x for x in D[i]
            if len([(x,y) in C[i][j] for y in D[j]])==0])
    if not empty(violate):
        D[i] = D[i] - violate
        return true, (X, D, C)
    return false, csp



def AC3(csp, queue):
    if empty(queue):
        return true
    (i, j) = queue.pop()
    revised, csp = Revise(csp, i, j)
    if revised:
        D = csp[1]
    if empty(D[i]): return false
    [queue.push( (k,i) ) for k in neighbors(i, csp) if k!=i]
    return AC3(csp, queue)
