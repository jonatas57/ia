import numpy  as np
import pygame as pg
import random as rd
from copy import deepcopy

boardSize = np.array([20, 10])
blockSize = 20

shapes = [
    [[1,1,1,1]],
    [[2,2],[2,2]],
    [[3,3,3],[0,3,0]],
    [[4,4,0],[0,4,4]],
    [[0,5,5],[5,5,0]],
    [[0,0,6],[6,6,6]],
    [[7,7,7],[0,0,7]]
]
colors = [
    (  0,   0,   0),
    (  0, 255, 255),
    (  0,   0, 255),
    (255, 125,   0),
    (255, 255,   0),
    (  0, 255,   0),
    (255,   0, 190),
    (255,   0,   0)
]

DROPEVENT   = pg.USEREVENT + 1
CREATEBLOCK = pg.USEREVENT + 2

moves = {
    "LEFT"  : np.array([0, -1]),
    "RIGHT" : np.array([0, 1]),
    "DOWN"  : np.array([1, 0]),
    "NONE"  : np.array([0, 0])
}

def newBlock(idx=-1):
    if idx <= -1 or idx >= 7:
        b = rd.choice(shapes)
    else:
        b = shapes[idx]
    r = rd.randint(0,3)
    b = np.rot90(b, r)
    return b, np.array([0, int((boardSize[1] - len(b[0])) / 2)])

def joinMat(m, n, pos):
    x, y = pos
    joined = deepcopy(m)
    for i in range(len(n)):
        for j in range(len(n[i])):
            joined[i + x][j + y] += n[i][j]
    return joined

class tetris:
    def __init__(self):
        pg.init()
        self.height, self.width = x, y = boardSize
        self.board = np.zeros(boardSize, dtype=np.int)
        self.rects = [[pg.Rect(j * blockSize, i * blockSize, blockSize, blockSize)
                                for j in range(y)]
                                for i in range(x)]
        self.blockFill = pg.Surface([blockSize] * 2);
        self.actualBlock, self.blockPos = newBlock()
        self.joined = joinMat(self.board, self.actualBlock, self.blockPos)
        self.speed = 1000
        self.drop = False

    def start(self):
        self.screen = pg.display.set_mode(boardSize[::-1] * blockSize, pg.RESIZABLE)
        pg.display.set_caption("Tetris")
        self.gameOver = False
        clock = pg.time.Clock()
        pg.time.set_timer(DROPEVENT, self.speed)
        while not self.gameOver:
            for event in pg.event.get():
                try:
                    self.handle(event)
                except:
                    self.gameOver = True
                    break
            if self.drop:
                self.move("DOWN")

            self.screen.fill((0, 0, 0))
            self.drawAll()
            pg.display.flip()
            clock.tick(30)

    def drawAll(self):
        self.joined = joinMat(self.board, self.actualBlock, self.blockPos)
        for i in range(self.height):
            for j in range(self.width):
                self.blockFill.fill(colors[self.joined[i][j] % 8])
                self.screen.blit(self.blockFill, self.rects[i][j])

    def rotateBlock(self):
        rotated = np.rot90(self.actualBlock)
        x, y = self.collision(dir="NONE", block=rotated)
        if x:
            return
        else:
            self.actualBlock = rotated

    def move(self, dir):
        col, new = self.collision(dir)
        if not col:
            self.blockPos += moves[dir]
        if new:
            self.drop = False
            pg.event.post(pg.event.Event(CREATEBLOCK))

    def collision(self, dir="NONE", block=None):
        if block is None: block = self.actualBlock
        x, y = self.blockPos
        dx, dy = moves[dir]
        bx, by = len(block), len(block[0])
        col = new = False
        nx, ny = x + dx, y + dy
        if ny < 0 or ny + by > self.width or nx + bx > self.height:
            col = True
        qtd = 0
        for i in range(bx):
            for j in range(by):
                try:
                    if block[i][j] and self.board[i + x + dx][j + y + dy]:
                        col = True
                        qtd += 1
                except IndexError:
                    col = True
        if col:
            if dir == "DOWN":
                new = True

        return col, new

    def checkLines(self):
        lines = []
        for i in range(self.height):
            qtd = 0
            for j in self.board[i]:
                if j != 0:
                    qtd += 1
            if qtd == self.width:
                lines.append(i)
        return lines

    def delLines(self, lines):
        if len(lines) == 0:
            return
        self.board[0] = np.zeros(self.width, dtype=np.int)
        for l in lines:
            for i in range(l, 1, -1):
                for j in range(self.width):
                    self.board[i][j] = self.board[i - 1][j]

    def handle(self, event):
        if event.type == pg.QUIT:
            self.gameOver = True
        elif event.type == DROPEVENT:
            self.move('DOWN')
        elif event.type == CREATEBLOCK:
            self.board = self.joined
            self.delLines(self.checkLines())
            self.actualBlock, self.blockPos = newBlock()
            if self.collision(dir="NONE")[0]:
                raise Exception("Game Over")
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.move('LEFT')
            elif event.key == pg.K_RIGHT:
                self.move('RIGHT')
            elif event.key == pg.K_UP:
                self.rotateBlock()
            elif event.key == pg.K_DOWN or self.drop:
                self.drop = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                self.drop = False

def main():
    x = tetris()
    x.start()

main()
