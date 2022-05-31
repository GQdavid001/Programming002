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
