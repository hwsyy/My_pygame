#codeing=utf-8
# @Time    : 2017-10-20
# @Author  : J.sky
# @Mail    : bosichong@qq.com
# @Site    : www.17python.com
# @Title   : # “编学编玩”用Pygame写游戏（3）让角色动起来及碰撞检测
# @Url     : http://www.17python.com/blog/46
# @Details : # “编学编玩”用Pygame写游戏（3）让角色动起来及碰撞检测
# @Other   : OS X 10.11.6 
#            Python 3.6.1
#            VSCode 1.15.1
###################################
# “编学编玩”用Pygame写游戏（3）让角色动起来及碰撞检测
###################################

'''
上次的代码中，除了绘制基本图形与图片外，中间还插入了一个小小动画，就是头像在不停的移动，这个移动确实简单了些，游戏中的的角色肯定不是简单的移动几像素那么简单了。

## 屡屡顺序

我觉得刚开始做游戏写代码的时候，总是弄不清游戏的顺序，你可以这样想象一下，比如是拍电影，大家都了解电影是一段一段拍，最后合成在一起然后电影可以播放了。
游戏呢和这个差不多，也是一段一段做，只不过游戏需要一些条件判断，True了，我就播放第三段，这个属性值达到了我就播放第五段，游戏over了，我就播放结尾。
好吧，那么我们规划一下现在这个小游戏（应该算不上是一个游戏）场景及角色。

## 游戏内容

建一个 640X480的黑色背景的游戏场景，场景中随机生成一些大小一样的小球，他们随机属性值，有一个绿色，有一组红色，如果绿色碰到红色他们就会反转滚动，这些小球如果碰到边界也会反转滚动。
注意：这里碰撞的检测之后的动作，只是简单的，并不是真的物理运动哦，当然如果你很懂物理学，做一组力学物理运动应该也不是很难的。

## 游戏场景

+ 游戏场景的搭建和之前基本上相信，这里不在介绍了，如果不了解可以翻看之前或是本节的代码参考。

## 游戏中的角色

之前我们在场景中是直接绘制的图形，这次我们通过面向对象的方式来管理场景中的角色，pygame中提供了一个`Sprite`类，这个类专门为游戏中的角色精灵准备的。
框架中还提供了一个`pygame.sprite.Group()`容器，他可以把sprite加进去，通过group来管理，group这个容器，通过查看源代码，他只能处理图片类型的sprite。
如果创建的Rect对象是不行的，这种加到组里后，通过draw是无法绘制出来的，`group.draw()`这个方法中的画笔使用了`blit()`，而不是`draw()`

## 游戏中的逻辑判断

这个我们直接在游戏中的循环当中直接判断，我是这么把游戏分成各种对象的：

+ 游戏场景对象，他只负责绘制场景中的任何角色及精灵
+ 游戏逻辑判断对象，他只负责判断游戏场景中的碰撞，时间检测，然后修改他们的属性。
+ 精灵group，他们只负责创建，删除。


## 开始制作

理论课结束，我们来实践一下，`main()`函数中创建一个游戏运行函数`rungame()`，这个函数中运行着当前游戏的所有数据，及各种事件触发的检测。
为什么需要`rungame()`?你可以把他这个函数看成一个电影片段，当前你还可以有`gamestart() gameover()`函数，这样游戏运行到哪个部位时就让哪个函数运行即可。


## Sprite 精灵

说说`class MyImgSprite(pygame.sprite.Sprite`，这是当前游戏中的精灵，我们为他创建了几个属性，其中比较重要的有：

    self.image = pygame.image.load('./images/a.png') #导入图片
    self.rect = self.image.get_rect() #返回一个rect对象
    self.rect.topleft = (random.randint(40,590),random.randint(40,430))#设置他的坐标  
    self.last_update = pygame.time.get_ticks()#获取当前游戏动行的时间，这是一个整数，不明白可以打印看看
    #移动速度
    self.speed_x = random.randint(1,10)
    self.speed_y = random.randint(1,10)

有了速度，我们就可以通过`update()`方法来更新自己的坐标

    now = pygame.time.get_ticks()
    if now - self.last_update >1:#通过这个时间差来做一些动画       
        #self.rect.topleft = (random.randint(0,600),random.randint(0,440))#随机变化位置
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.last_update = now

如果你不在`update()`方法更新任何值，那么 这个表灵就是不会动弹的。
那么问题来了，为什么不直接在游戏循环中更新？
上节的代码中有段小小的移动是在循环中更新的，因为那只有一段动画，如果以后有很多个对象的话，在循环中更新会很麻烦，这里更新更符合面向对象的的编程方式。

## 绘制及更新

在rungame函数中创建个绿球，一组红球，然后就可以直接在场景里绘制了，绘制方法：

    drawbackground()#绘制场景背景颜色
    DISPLAYSURF.blit(m.image,m.rect)#绘制绿球
    myimgs.draw(DISPLAYSURF)#绘制一组红球 

场景中的绘制顺序应该是：

1. 绘制精灵
2. 逻辑判断
3. udpate()更新数据

以此为循环，这样反复循环即可生成画面。

## 逻辑判断

说到逻辑判断，这次场景中包括的判断有二种：边界碰撞及球体之间的碰撞。
边界碰撞，我自个写了个边界碰撞检测器`BorderCrossing.py`，因为我在pygame中没找到边界碰撞检测的方法，大家在运行代码的时候，记得git clone一下整个项目。
这个边界碰撞检测器，我就不多说了，不然这又一篇博客了，有兴趣可以自己看看源码。

球体之间的碰撞检测直接套用的pygame中的碰撞检测，具体可以参考官方文档

[碰撞检测官方文档](http://pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide)

## 更新游戏数据

在逻辑判断中根据自己的需要进行速度等数据修改，最后记得用方法更新一下精灵们的坐标。
说的不是很好，具体大家跑跑程序，改改数值就明白了，如果有什么不懂的，可以直接留言或是邮件给我。



'''







import pygame, sys, random
from os import path
from pygame.locals import * #导入游戏常量
from PY_RPG.BorderCrossing import *


#一些游戏资源加载及设置
FPS = 30#帧速率
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
WHITE = (255,255,255,)
pygame.display.set_caption("Hello World!")#窗口标题
BLACK = (0,0,0)
######################
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()#游戏初始化
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),DOUBLEBUF,32)#设置游戏场景游戏大小
    #####游戏循环
    while True:
        runGame()

def runGame():
    '''游戏核心方法，渲染游戏场景，游戏逻辑判断等'''
    m = MyImgSprite()#创建一个精灵对象
    m.image=pygame.image.load('./images/b.png')

    #创建一组精灵对象
    myimgs = pygame.sprite.Group()
    for i in range(7):
        myimgs.add(MyImgSprite())
    print(len(myimgs))
    #创建一个边界碰撞检对象
    bc = BorderCrossing(5,5,SCREEN_WIDTH-10,SCREEN_HEIGHT-10)
    
    #######游戏引擎设置：判断游戏结束，更新游戏，刷新帧速率设置
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        ############
        drawbackground()#绘制场景背景颜色
        DISPLAYSURF.blit(m.image,m.rect)#绘制绿球
        myimgs.draw(DISPLAYSURF)#绘制一组红球 

        #绿球边界碰撞检测
        bc.sprite = m.rect
        if bc.isTopBorderCrossing() or bc.isBottomBorderCrossing():
            m.speed_y = -m.speed_y
        if bc.isLeftBorderCrossing() or bc.isRightBorderCrossing():
            m.speed_x = -m.speed_x

        #红绿边界碰撞检测
        for sp in myimgs:
                bc.sprite = sp.rect
                if bc.isTopBorderCrossing() or bc.isBottomBorderCrossing():
                    sp.speed_y = -sp.speed_y
                if bc.isLeftBorderCrossing() or bc.isRightBorderCrossing():
                    sp.speed_x = -sp.speed_x
        #绿球与红球碰撞检测        
        for m1 in myimgs:
            k = pygame.sprite.collide_rect(m,m1)
            if k :
                m.speed_x = -m.speed_x
                m.speed_y = -m.speed_y
                m1.speed_x = -m1.speed_x
                m1.speed_y = -m1.speed_y
        # rst = list_collide = pygame.sprite.spritecollide(m,myimgs,True)
        #true,碰到后直接删除， false会删除Group组中的精灵。
        #########################################
        #红球之间的碰撞检测
        ####################
        for s1 in myimgs:
            for s2 in myimgs:
                if s1.rect.x != s2.rect.x: #判断不是同一个sprite
                    print('不是同一个精灵')
                    if pygame.sprite.collide_rect(s1, s2):#碰撞检测
                        print(s1.rect, s2.rect)
                        s2.speed_x = -s2.speed_x
                        s2.speed_y = -s2.speed_y
                        s1.speed_x = -s1.speed_x
                        s1.speed_y = -s1.speed_y
                        myimgs.update()#这里需要立即更新红球的坐标
                            
                    
        m.update()#更新绿球
        myimgs.update()#更新红球Group

        pygame.display.flip()
        FPSCLOCK.tick(FPS)#设置帧速率
def drawbackground():
    '''绘制游戏背景'''
    DISPLAYSURF.fill(BLACK)#游戏窗口背景色

class MyImgSprite(pygame.sprite.Sprite):
    '''图片精灵类'''
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load('./images/a.png') #导入图片
       self.rect = self.image.get_rect() #返回一个rect对象
       self.rect.topleft = (random.randint(40,590),random.randint(40,430))#设置他的坐标  
       self.last_update = pygame.time.get_ticks()#获取当前游戏动行的时间，这是一个整数，不明白可以打印看看
       #移动速度
       self.speed_x = random.randint(1,10)
       self.speed_y = random.randint(1,10)

    def update(self):
        '''更新自己的坐标，如果放在精灵组中，调用组的update()函数，会自动调用本函数'''
        now = pygame.time.get_ticks()
        if now - self.last_update >1:#通过这个时间差来做一些动画       
            # self.rect.topleft = (random.randint(0,600),random.randint(0,440))#随机变化位置
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.last_update = now

if __name__ == '__main__':
    main()
