#常量 constant
W,H = 288,512
FPS = 30 #frames per second

pygame.init() #初始化pygame，使得pygame可以为程序员所用
SCREEN = pygame.display.set_mode((W,H))
pygame.display.set_caption('flappy bird by lmr')
CLOCK = pygame.time.Clock()


#图形素材
IMAGES = {} #建立空字典
for image in os.listdir(r"C:\Users\86156\Desktop\pycharm项目\sprites"): #listdir函数可以列举出文件夹中所有的文件名，注意，该文件名是相对文件夹下的名字
    name,extension = os.path.splitext(image)     #splitext函数可以将文件拆分成文件名+后缀
    path = os.path.join(r"C:\Users\86156\Desktop\pycharm项目\sprites",image)
    IMAGES[name] = pygame.image.load(path) #构建字典的映射（键值对）关系

floor_y = H - IMAGES['floor'].get_height()

bird = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\red-mid.png")
bgpic = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\day.png")
guide = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\guide.png")
floor = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\floor.png")
pipe = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\green-pipe.png")
gameover = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\gameover.png")

#音乐素材
START = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\start.wav")
DIE = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\die.wav")
HIT = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\hit.wav")
SCORE = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\score.wav")
FLAP = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\flap.wav")

class Bird:
    def __init__(self,x,y):
        self.frames = [0]*5 + [1]*5 + [2]*5 + [1]*5
        self.idx = 0
        self.images = IMAGES['birds']
        self.image = self.images[self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0
        self.max_y_vel = 10
        self.gravity = 1
        self.rotate = 45
        self.max_rotate = -20
        self.rotate_vel = -3
        self.y_vel_after_flap = -10
        self.rotate_after_flap = 45

    def update(self,flap=False):
        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap
        self.y_vel = min(self.y_vel + self.gravity,self.max_y_vel)
        self.rect.y += self.y_vel
        self.rotate = max(self.rotate+self.rotate_vel,self.max_rotate)

        self.idx += 1
        self.idx %= len(self.frames)
        self.image = IMAGES['birds'][self.frames[self.idx]]
        self.image = pygame.transform.rotate(self.image,self.rotate)

    def go_die(self):
        if self.rect.y < floor_y:
            self.rect.y += self.max_y_vel
            self.rotate = -90
            self.image = self.images[self.frames[self.idx]]
            self.image = pygame.transform.rotate(self.image,self.rotate)


class Pipe(pygame.sprite.Sprite): #让水管类继承精灵类的方法
    def __init__(self,x,y,upwards=True):#upwards变量标志着水管是上面还是下面出现
        pygame.sprite.Sprite.__init__(self)
        if upwards:
            self.image = IMAGES['pipes'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top= y
        else:
            self.image = IMAGES['pipes'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y

        self.x_vel = -4
    def update(self):
        self.rect.x += self.x_vel

        def main():
    while True:
        START.play()
        IMAGES['bgpic'] = IMAGES[random.choice(['day','night'])]
        color = random.choice(['red','yellow','blue'])
        IMAGES['birds'] = [IMAGES[color+'-up'],IMAGES[color+'-mid'],IMAGES[color+'-down']]
        pipe = IMAGES[random.choice(['green-pipe','red-pipe'])]
        IMAGES['pipes'] = [pipe,pygame.transform.flip(pipe,False,True)]
        menu_window()
        result = game_window()
        end_window(result)

def menu_window():
    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0
    guide_x = (W - IMAGES['guide'].get_width()) / 2
    guide_y = (floor_y - IMAGES['guide'].get_height()) / 2
    bird_x = W * 0.2
    bird_y = (H - IMAGES['birds'][0].get_height()) / 2
    bird_y_vel = 1 #代表小鸟一个帧数内移动的像素（简单来说就是小鸟漂浮的速度）
    bird_y_range = [bird_y - 8,bird_y + 8] #代表小鸟在y方向上移动的范围
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0



        bird_y += bird_y_vel
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1


        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        SCREEN.blit(IMAGES['floor'],(floor_x, floor_y))
        SCREEN.blit(IMAGES['guide'], (guide_x, guide_y))
        SCREEN.blit(IMAGES['birds'][0], (bird_x, bird_y))
        pygame.display.update()
        CLOCK.tick(FPS)


def game_window():
    score = 0 #初始化分数为零
    FLAP.play()
    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0


    bird = Bird(W * 0.2 , H * 0.4) #生成小鸟对象


    distance = 150 #水管之间的距离
    n_pairs = 4 #水管对的数目
    pipe_gap = 100 #上下水管的间距
    pipe_group = pygame.sprite.Group()#使用精灵中的群组类
    for i in range(n_pairs):
        pipe_y = random.randint(int(H*0.3),int(H*0.7)) #利用随机函数随机生成每个管子的高度
        pipe_up = Pipe(W+i*distance,pipe_y,True)
        pipe_down =  Pipe(W+i*distance,pipe_y - pipe_gap,True)
        pipe_group.add(pipe_up)
        pipe_group.add(pipe_down)



    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    flap = True
                    FLAP.play()

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0

        bird.update(flap)
        first_pipe_up = pipe_group.sprites()[0]
        first_pipe_down = pipe_group.sprites()[1]
        if first_pipe_up.rect.right<0:

            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
            new_pipe_up = Pipe(first_pipe_up.rect.x + n_pairs*distance,pipe_y,True)
            new_pipe_down = Pipe(first_pipe_down.rect.x +n_pairs*distance,pipe_y - pipe_gap,False)
            pipe_group.add(new_pipe_up)
            pipe_group.add(new_pipe_down)
            first_pipe_up.kill()
            first_pipe_down.kill()


        pipe_group.update() #自动执行精灵组中每个精灵的update方法

#碰撞检测
        if bird.rect.y > floor_y or bird.rect.y < 0:
            HIT.play()
            DIE.play()
            result = {'bird': bird, 'pipe_group': pipe_group,'score':score} # 构建一个结果字典，将鸟类状态与当前死亡时候的管道状态传递给游戏结束界面
            return result

        for pipe in pipe_group.sprites():
            right_to_left = max(bird.rect.right,pipe.rect.right) - min(bird.rect.left,pipe.rect.left)
            bottom_to_top = max(bird.rect.bottom,pipe.rect.bottom) - min(bird.rect.top,pipe.rect.top)
            if right_to_left < bird.rect.width+pipe.rect.width and bottom_to_top < bird.rect.height + pipe.rect.height:
                HIT.play()
                DIE.play()
                result = {'bird': bird,'pipe_group':pipe_group,'score':score}
                return result




        if bird.rect.left + first_pipe_up.x_vel<first_pipe_up.rect.centerx<bird.rect.left:
            SCORE.play()
            score += 1



        SCREEN.blit(IMAGES['bgpic'],(0,0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (floor_x, floor_y))
        #score1 = 999
        show_score(score)
        SCREEN.blit(bird.image,(bird.rect.x,bird.rect.y))
        pygame.display.update()
        CLOCK.tick(FPS)

def end_window(result):
    gameover_x = (W - gameover.get_width()) / 2
    gameover_y = (floor_y - gameover.get_height()) / 2

    bird = result['bird']
    pipe_group = result['pipe_group']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        bird.go_die()
        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (0, floor_y))
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        show_score(result['score'])
        SCREEN.blit(bird.image,bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)
def show_score(score):
    score_str = str(score)
    n = len(score_str)
    w = IMAGES['0'].get_width() * 1.1
    x = (W - n * w) / 2
    y = H * 0.1
    for number in score_str:
        SCREEN.blit(IMAGES[number], (x, y))
        x += w

整体模块效果：
import pygame
import random
import time
import os



#常量 constant
W,H = 288,512
FPS = 30 #frames per second

pygame.init() #初始化pygame，使得pygame可以为程序员所用
SCREEN = pygame.display.set_mode((W,H))
pygame.display.set_caption('flappy bird by lmr')
CLOCK = pygame.time.Clock()


#图形素材
IMAGES = {} #建立空字典
for image in os.listdir(r"C:\Users\86156\Desktop\pycharm项目\sprites"): #listdir函数可以列举出文件夹中所有的文件名，注意，该文件名是相对文件夹下的名字
    name,extension = os.path.splitext(image)     #splitext函数可以将文件拆分成文件名+后缀
    path = os.path.join(r"C:\Users\86156\Desktop\pycharm项目\sprites",image)
    IMAGES[name] = pygame.image.load(path) #构建字典的映射（键值对）关系

floor_y = H - IMAGES['floor'].get_height()

bird = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\red-mid.png")
bgpic = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\day.png")
guide = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\guide.png")
floor = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\floor.png")
pipe = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\green-pipe.png")
gameover = pygame.image.load(r"C:\Users\86156\Desktop\pycharm项目\sprites\gameover.png")

#音乐素材
START = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\start.wav")
DIE = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\die.wav")
HIT = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\hit.wav")
SCORE = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\score.wav")
FLAP = pygame.mixer.Sound(r"C:\Users\86156\Desktop\pycharm项目\audio\flap.wav")

def main():
    while True:
        START.play()
        IMAGES['bgpic'] = IMAGES[random.choice(['day','night'])]
        color = random.choice(['red','yellow','blue'])
        IMAGES['birds'] = [IMAGES[color+'-up'],IMAGES[color+'-mid'],IMAGES[color+'-down']]
        pipe = IMAGES[random.choice(['green-pipe','red-pipe'])]
        IMAGES['pipes'] = [pipe,pygame.transform.flip(pipe,False,True)]
        menu_window()
        result = game_window()
        end_window(result)

def menu_window():
    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0
    guide_x = (W - IMAGES['guide'].get_width()) / 2
    guide_y = (floor_y - IMAGES['guide'].get_height()) / 2
    bird_x = W * 0.2
    bird_y = (H - IMAGES['birds'][0].get_height()) / 2
    bird_y_vel = 1 #代表小鸟一个帧数内移动的像素（简单来说就是小鸟漂浮的速度）
    bird_y_range = [bird_y - 8,bird_y + 8] #代表小鸟在y方向上移动的范围
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0



        bird_y += bird_y_vel
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1


        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        SCREEN.blit(IMAGES['floor'],(floor_x, floor_y))
        SCREEN.blit(IMAGES['guide'], (guide_x, guide_y))
        SCREEN.blit(IMAGES['birds'][0], (bird_x, bird_y))
        pygame.display.update()
        CLOCK.tick(FPS)


def game_window():
    score = 0 #初始化分数为零
    FLAP.play()
    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0


    bird = Bird(W * 0.2 , H * 0.4) #生成小鸟对象


    distance = 150 #水管之间的距离
    n_pairs = 4 #水管对的数目
    pipe_gap = 100 #上下水管的间距
    pipe_group = pygame.sprite.Group()#使用精灵中的群组类
    for i in range(n_pairs):
        pipe_y = random.randint(int(H*0.3),int(H*0.7)) #利用随机函数随机生成每个管子的高度
        pipe_up = Pipe(W+i*distance,pipe_y,True)
        pipe_down =  Pipe(W+i*distance,pipe_y - pipe_gap,True)
        pipe_group.add(pipe_up)
        pipe_group.add(pipe_down)



    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    flap = True
                    FLAP.play()

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0

        bird.update(flap)
        first_pipe_up = pipe_group.sprites()[0]
        first_pipe_down = pipe_group.sprites()[1]
        if first_pipe_up.rect.right<0:

            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
            new_pipe_up = Pipe(first_pipe_up.rect.x + n_pairs*distance,pipe_y,True)
            new_pipe_down = Pipe(first_pipe_down.rect.x +n_pairs*distance,pipe_y - pipe_gap,False)
            pipe_group.add(new_pipe_up)
            pipe_group.add(new_pipe_down)
            first_pipe_up.kill()
            first_pipe_down.kill()


        pipe_group.update() #自动执行精灵组中每个精灵的update方法

#碰撞检测
        if bird.rect.y > floor_y or bird.rect.y < 0:
            HIT.play()
            DIE.play()
            result = {'bird': bird, 'pipe_group': pipe_group,'score':score} # 构建一个结果字典，将鸟类状态与当前死亡时候的管道状态传递给游戏结束界面
            return result

        for pipe in pipe_group.sprites():
            right_to_left = max(bird.rect.right,pipe.rect.right) - min(bird.rect.left,pipe.rect.left)
            bottom_to_top = max(bird.rect.bottom,pipe.rect.bottom) - min(bird.rect.top,pipe.rect.top)
            if right_to_left < bird.rect.width+pipe.rect.width and bottom_to_top < bird.rect.height + pipe.rect.height:
                HIT.play()
                DIE.play()
                result = {'bird': bird,'pipe_group':pipe_group,'score':score}
                return result




        if bird.rect.left + first_pipe_up.x_vel<first_pipe_up.rect.centerx<bird.rect.left:
            SCORE.play()
            score += 1



        SCREEN.blit(IMAGES['bgpic'],(0,0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (floor_x, floor_y))
        #score1 = 999
        show_score(score)
        SCREEN.blit(bird.image,(bird.rect.x,bird.rect.y))
        pygame.display.update()
        CLOCK.tick(FPS)

def end_window(result):
    gameover_x = (W - gameover.get_width()) / 2
    gameover_y = (floor_y - gameover.get_height()) / 2

    bird = result['bird']
    pipe_group = result['pipe_group']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        bird.go_die()
        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (0, floor_y))
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        show_score(result['score'])
        SCREEN.blit(bird.image,bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)
def show_score(score):
    score_str = str(score)
    n = len(score_str)
    w = IMAGES['0'].get_width() * 1.1
    x = (W - n * w) / 2
    y = H * 0.1
    for number in score_str:
        SCREEN.blit(IMAGES[number], (x, y))
        x += w

class Bird:
    def __init__(self,x,y):
        self.frames = [0]*5 + [1]*5 + [2]*5 + [1]*5
        self.idx = 0
        self.images = IMAGES['birds']
        self.image = self.images[self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0
        self.max_y_vel = 10
        self.gravity = 1
        self.rotate = 45
        self.max_rotate = -20
        self.rotate_vel = -3
        self.y_vel_after_flap = -10
        self.rotate_after_flap = 45

    def update(self,flap=False):
        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap
        self.y_vel = min(self.y_vel + self.gravity,self.max_y_vel)
        self.rect.y += self.y_vel
        self.rotate = max(self.rotate+self.rotate_vel,self.max_rotate)

        self.idx += 1
        self.idx %= len(self.frames)
        self.image = IMAGES['birds'][self.frames[self.idx]]
        self.image = pygame.transform.rotate(self.image,self.rotate)

    def go_die(self):
        if self.rect.y < floor_y:
            self.rect.y += self.max_y_vel
            self.rotate = -90
            self.image = self.images[self.frames[self.idx]]
            self.image = pygame.transform.rotate(self.image,self.rotate)


class Pipe(pygame.sprite.Sprite): #让水管类继承精灵类的方法
    def __init__(self,x,y,upwards=True):#upwards变量标志着水管是上面还是下面出现
        pygame.sprite.Sprite.__init__(self)
        if upwards:
            self.image = IMAGES['pipes'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top= y
        else:
            self.image = IMAGES['pipes'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y

        self.x_vel = -4
    def update(self):
        self.rect.x += self.x_vel
