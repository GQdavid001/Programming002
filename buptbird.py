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
