import pygame, sys, random
from tkinter import messagebox

pygame.init()
black, white, green, blue, red = (0, 0, 0), (255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 0, 0)
scW, scH = 960, 640
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("Connect 4")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()
foodpics = [pygame.image.load('apple.png'), pygame.image.load('orange.png'), pygame.image.load('mango.png'), pygame.image.load('banana.png')]
play, autoplay, paused = True, False, True
speed, activespeed = 10, 1
autoplaybox, speedbox0, speedbox1, speedbox2, speedbox3 = pygame.Rect(30, 10, 160, 30), pygame.Rect(730, 10, 50, 30), pygame.Rect(790, 10, 40, 30), pygame.Rect(840, 10, 40, 30), pygame.Rect(890, 10, 40, 30)
font = pygame.font.SysFont('inkfree', 20, 2)
textposx, textposy = 40, 12
food = random.choice(foodpics)

def buttons(pos = None):
    global autoplay, activespeed, speed
    if pos:
        if autoplaybox.collidepoint(pos): autoplay = True if not autoplay else False
        elif speedbox0.collidepoint(pos): activespeed = 0
        elif speedbox1.collidepoint(pos): activespeed = 1
        elif speedbox2.collidepoint(pos): activespeed = 2
        elif speedbox3.collidepoint(pos): activespeed = 3

    if not autoplay:
        pygame.draw.rect(screen, red, autoplaybox, 2)
        text = font.render('AutoPlay: Off', True, red)
    else:
        pygame.draw.rect(screen, green, autoplaybox, 2)
        text = font.render('AutoPlay: On', True, green)
    screen.blit(text, (textposx, textposy))

    if activespeed == 0:
        pygame.draw.rect(screen, green, speedbox0, 2)
        text = font.render('0.5x', True, green)
        speed = 5
    else:
        pygame.draw.rect(screen, red, speedbox0, 2)
        text = font.render('0.5x', True, red)
    screen.blit(text, (textposx+695, textposy))

    if activespeed == 1:
        pygame.draw.rect(screen, green, speedbox1, 2)
        text = font.render('1x', True, green)
        speed = 10
    else:
        pygame.draw.rect(screen, red, speedbox1, 2)
        text = font.render('1x', True, red)
    screen.blit(text, (textposx+760, textposy))
    
    if activespeed == 2:
        pygame.draw.rect(screen, green, speedbox2, 2)
        text = font.render('2x', True, green)
        speed = 20
    else:
        pygame.draw.rect(screen, red, speedbox2, 2)
        text = font.render('2x', True, red)
    screen.blit(text, (textposx+805, textposy))
    
    if activespeed == 3:
        pygame.draw.rect(screen, green, speedbox3, 2)
        text = font.render('4x', True, green)
        speed = 40
    else:
        pygame.draw.rect(screen, red, speedbox3, 2)
        text = font.render('4x', True, red)
    screen.blit(text, (textposx+855, textposy))

def game_over():
    global play
    play = False
    if len(mysnake.body) != 15*25: messagebox.showinfo("Game Over", "You did your best mate, GG!")
    else: messagebox.showinfo("You Win", "Congrats! You won this shitty version of Snake!")

class Segment:
    def __init__(self, i, j, nex = None):
        self.i = i
        self.j = j
        self.next = nex

    def __str__(self):
        if self.next == None: return 'head'
        return str((self.i, self.j))

class Snake:
    def __init__(self):
        self.body = [Segment(7, 12)]
        self.direction = 'down'
        self.a = set([(i, j) for j in range(25) for i in range(15)])
        self.food = random.choice(list(self.a))

    def __repr__(self):
        return str([(seg.i, seg.j) for seg in self.body])

    def grow(self):
        new = Segment(self.body[-1].i, self.body[-1].j, self.body[-1])
        self.body.append(new)
    
    def move(self):
        try:
            for seg in self.body[1:][::-1]:
                seg.i, seg.j = seg.next.i, seg.next.j
            if self.direction == 'down': self.body[0].i += 1
            elif self.direction == 'up': self.body[0].i -= 1
            elif self.direction == 'left': self.body[0].j -= 1
            elif self.direction == 'right': self.body[0].j += 1
        except:
            game_over()
            return
        self.check_dead()
        self.check_eaten()

    def check_eaten(self):
        global food
        loc = (mygrid.boxes[self.food[0]][self.food[1]].position.x+3, mygrid.boxes[self.food[0]][self.food[1]].position.y+3)
        screen.blit(food, loc)
        if self.food == (self.body[0].i, self.body[0].j):
            b = set([(seg.i, seg.j) for seg in self.body])
            self.a -= b
            self.food = random.choice(list(self.a))
            self.grow()
            food = random.choice(foodpics)

    def check_dead(self):
        i, j = self.body[0].i, self.body[0].j
        for seg in self.body[1:]:
            if (seg.i, seg.j) == (i, j):
                game_over()
                return
        if i < 0 or i > 14 or j < 0 or j > 24:
            game_over()
            return

    def blocked(self, i, j):
        if i < 0 or i > 14 or j < 0 or j > 24: return True
        for seg in self.body:
            if (i, j) == (seg.i, seg.j): return True
        return False

    def direct(self):
        dist = lambda x, y: abs(x - self.food[0]) + abs(y - self.food[1])
        i, j = self.body[0].i, self.body[0].j
        moves = {}
        if not self.blocked(i+1, j): moves['down'] = dist(i+1, j)
        if not self.blocked(i-1, j): moves['up'] = dist(i-1, j)
        if not self.blocked(i, j+1): moves['right'] = dist(i, j+1)
        if not self.blocked(i, j-1): moves['left'] = dist(i, j-1)
        if moves:
            idx = min(moves, key=lambda x: moves[x])
            self.direction = idx

class Box:
    def __init__(self, i, j, buffX, buffY, blocksize):
        self.i = i
        self.j = j
        self.position = pygame.Rect(buffX+(self.j*(blocksize+(blocksize*0.2))), buffY+(self.i*(blocksize+(blocksize*0.2))), blocksize, blocksize)

    def show(self):
        pygame.draw.rect(screen, white, self.position, 1)

class Grid:
    def __init__(self, rows, columns, snake, blocksize=30):
        buffX, buffY = int((scW/2)-(((blocksize+(blocksize*0.2))*columns)/2)), int((scH/2)-(((blocksize+(blocksize*0.2))*rows)/2))
        self.boxes = [[Box(i, j, buffX, buffY, blocksize) for j in range(columns)] for i in range(rows)]
        self.gridify = False
        self.position = pygame.Rect(buffX, buffY, (blocksize*columns)+((blocksize*columns)//5), (blocksize*rows)+((blocksize*rows)//5))
        self.snake = snake

    def show(self):
        if self.gridify:
            for line in self.boxes:
                for box in line:
                    box.show()
        else:
            pygame.draw.rect(screen, white, self.position, 3)
        
        buttons()
        if not paused: self.snake.move()
        else: screen.blit(font.render('Paused', True, red), (500, 12))
        [pygame.draw.rect(screen, white, self.boxes[seg.i][seg.j].position) for seg in self.snake.body]            

mysnake = Snake()
mygrid = Grid(15, 25, mysnake)

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()
            if event.key == pygame.K_p: paused = True if not paused else False
            if event.key == pygame.K_SPACE: autoplay = True if not autoplay else False
            if event.key == pygame.K_0: activespeed = 0
            if event.key == pygame.K_1: activespeed = 1
            if event.key == pygame.K_2: activespeed = 2
            if event.key == pygame.K_3: activespeed = 3
            if not autoplay:
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and mysnake.direction != 'up': mysnake.direction = 'down'
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and mysnake.direction != 'down': mysnake.direction = 'up'
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and mysnake.direction != 'left': mysnake.direction = 'right'
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and mysnake.direction != 'right': mysnake.direction = 'left'
        if event.type == pygame.MOUSEBUTTONDOWN: buttons(pygame.mouse.get_pos())
    
    if autoplay: mysnake.direct()

    screen.fill(black)
    mygrid.show()
    pygame.display.flip()
    clock.tick(speed)

sys.exit()