import pygame
import time
import sys
import math

class make_sprite(pygame.sprite.Sprite):
    def __init__(self, func, path: str, position_x: int, position_y: int, widthScale: int, heightScale: int, damage: int, isFlip:float,  n: list):
        super().__init__()
        self.function = func
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (image.get_width()*widthScale, image.get_height()*heightScale))
        self.image = pygame.transform.flip(image, flip_x=isFlip, flip_y=0).convert_alpha()
        self.rect = self.image.get_rect(center=(position_x+n[0], position_y+n[1]))
        self.damage=damage
    def update(self):
        self.function() 
def do_nothing():
    pass
            
def make_animsprite(name: str, extension: str, n:int, data: list)->list: #dict -> num: value
    """[quantity: int, position_x: int, position_y: int, width: int, height: int, damage: int]
    
        _Args:
        path (str): _description_
        extension (str): _description_
        n (int): _description_
        data (list): _description_

    Returns:
        list: _description_
    """
    count=1
    mySprites=[]
    for i in data:                  #[quantity: int, position_x: int, position_y: int, width: int, height: int, damage: int, n: list <x,y>]
        for x in range(count, i[0]+1):
            mySprites.append(make_sprite(path=f"{name}{x}{extension}", func=do_nothing, position_x=i[1], position_y=i[2], widthScale=i[3], heightScale=i[4], damage=i[5], isFlip=i[6], n=i[7]))
        count=x+1
    if n==len(mySprites):
        return mySprites
    else:
        raise "There is something wrong!"    

class Player(pygame.sprite.Sprite):
    def __init__(self, *, health: int, name: str):#Must keywoard arguments
        super().__init__()
        self.width = 50
        self.height = 50
        self.image = pygame.transform.smoothscale(pygame.image.load("asset/plane.png"), (self.width,self.height)).convert_alpha()
        self.position_x=400
        self.position_y=530
        self.rect = self.image.get_rect(center=(self.position_x, self.position_y))
        self.health = health
        self.name = name
        self.mask = pygame.mask.from_surface(self.image)
    def take_hit(self, damage_take: int):
        global barPlayerHealth, isPlayerAlive
        self.health-=damage_take
        if self.health<=0:
            isPlayerAlive=False
            return None
        barPlayerHealth=pygame.transform.scale(surface=barPlayerHealth, size=(round(150*player.health/player_health),20))
        
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, *, position_x, position_y, speed, damage):
            """Use posistion x for half/center of weidht of player image and half/center height for position y
            
            USE EVEN NUMBER    
                """
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load("asset/bullet.png"), (26,26)).convert_alpha()
            self.rect = self.image.get_rect(center=(position_x, position_y)) #Rect -> x, y, widht, height
            self.speed = speed
            self.damage = damage
        
        def update(self):
            self.rect.y-= self.speed
            if self.rect.bottom < 0: #kill the bullet if it left the border
                self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self, *, health: int, position_x: int, position_y: int):
        super().__init__()
        self.health = health
        self.image = pygame.transform.scale(pygame.image.load("asset/iconofsin.png"), (202,89)).convert_alpha()
        self.rect = self.image.get_rect(center=(position_x, position_y))
        self.mask = pygame.mask.from_surface(self.image)
        
    def take_hit(self, damage_dealt: int):
        global barBossHealth, isBossAlive
        self.health-=damage_dealt
        if self.health<=0:
            self.kill()
            isBossAlive = False
            return "win"
        barBossHealth=pygame.transform.scale(surface=barBossHealth, size=(round(360*myBoss.health/boss_health),40))
    
    class BossBullets(pygame.sprite.Sprite):
        def __init__(self, *, damage: int, position_x: int, position_y: int, speed: float, width: int, height: int):
            super().__init__()
            self.damage = damage
            self.width = width
            self.height = height
            self.image = pygame.transform.scale(pygame.image.load("asset/laser_bullet.png"), (self.width, self.height)).convert_alpha()
            self.rect = self.image.get_rect(center=(position_x, position_y)) #Rect -> x, y, widht, height
            self.speed = speed
        def update(self):
            self.rect.y+= self.speed
            if self.rect.top > 600: #kill the bullet if it left the border
                self.kill()
    
    class CircleBullet(pygame.sprite.Sprite):
        def __init__(self, *, damage: int, position_x: int, position_y: int, distance: int, width: int, angle: int|float, isLeft: bool):
            super().__init__()
            self.width = width
            self.height = width
            self.damage = damage
            self.distance = distance
            self.image = pygame.transform.scale(pygame.image.load("asset/circle_bullet.png"), (self.width, self.height)).convert_alpha()
            self.rect = self.image.get_rect(center=(position_x, position_y))
            self.angle = angle
            self.count = 0
            self.num = 3 if isLeft else -3
            
        def update(self):
            self.rect.y += abs(round(self.distance*math.sin(self.angle*(math.pi/180))))
            self.rect.x += round(self.distance*math.cos(self.angle*(math.pi/180))) - self.count//self.num
            if 0<self.rect.bottom <600 and 0<self.rect.left <800 and 0<self.rect.right <800: #kill the bullet if it left the border
                self.count+=0.05
                pass 
            else:
                self.kill()
                
    def make_circle(self, group: pygame.sprite.Group, coordinates_x: list[int], coordinates_y: list[int], angles: list, isLeft: int):
        n=len(coordinates_x)
        for i in range(n):
            group.add(self.CircleBullet(damage=10, position_x=coordinates_x[i], position_y=coordinates_y[i], distance=5, width=20, angle=angles[i], isLeft=isLeft))
        multipleBulletSE.play()
            
    class Cannon():
        def __init__(self, *, position_x, position_y, widthScale:float, heightScale:float, isFlip: bool=False, damage: int):
            super().__init__()
            self.position_x = position_x
            self.position_y = position_y
            self.timer = None
            self.type = None
            self.cannon_counter = None
            self.animate = False
            self.isFlip = isFlip
            self.damage=damage
            n=18
            if isFlip:
                self.anim_x = -68
                self.num = 1
                data = [
                    [1, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [0,0]],
                    [2, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [5,-12]],
                    [3, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [10,-8]],
                    [6, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [15,5]],
                    [8, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [0,-8]],
                    [9, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-5,-5]],
                    [10, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [10,5]],
                    [12, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [12,8]],
                    [14, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-5,0]],
                    [15, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [5,4]],
                    [17, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [8,6]],
                    [18, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [0,0]],#The 18th is default or idle image
                ] #[quantity: int, position_x: int, position_y: int, width: int, height: int, damage: int, n: list <x,y>]
            else:
                self.anim_x = 800
                self.num = -1
                data = [
                    [2, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [0,0]],
                    [3, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-5,-5]],
                    [6, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-15,5]],
                    [8, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [0,-5]],
                    [9, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-5,-5]],
                    [10, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-10,5]],
                    [12, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-12,8]],
                    [14, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [0,-5]],
                    [15, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-5,5]],
                    [17, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [-8,8]],
                    [18, self.position_x, self.position_y, widthScale, heightScale, 0, isFlip, [0,0]],#The 18th is default or idle image
                ] #[quantity: int, position_x: int, position_y: int, width: int, height: int, damage: int, n: list <x,y>]
            self.cannon_sprite: list[pygame.sprite.Sprite] = make_animsprite(name="asset/cannon/image", extension=".png", n=n, data=data)

        class cannon_bullet(pygame.sprite.Sprite):
            def __init__(self, *, damage, position_x, position_y, width, height, distance, type: int, isFlip:bool):
                super().__init__()
                self.damage = damage
                self.width = width
                self.height = height #C:\Homework\Belajar\MyPygame\asset\cannon\canon_bullet.png
                self.image = pygame.transform.scale(pygame.image.load("asset/cannon/cannon_bullet.png"), (self.width, self.height)).convert_alpha()
                self.rect = self.image.get_rect(center=(position_x, position_y)) #Rect -> x, y, widht, height
                self.distance = distance
                self.angle = [244, 225, 215][type] #dari besar ke kecil
                self.isFlip = isFlip
            def update(self):
                self.rect.y += -1*round(self.distance*math.sin(self.angle*(math.pi/180)))
                if self.isFlip:
                    self.rect.x += -1*round(self.distance*math.cos(self.angle*(math.pi/180))) 
                else:
                    self.rect.x += round(self.distance*math.cos(self.angle*(math.pi/180))) 
                if 0<self.rect.bottom <600 and 0<self.rect.left <800 and 0<self.rect.right <800: #kill the bullet if it left the border
                    pass 
                else:
                    self.kill()
                    
        def cannon_showself(self, screen:pygame.surface.Surface):
            my_image = self.cannon_sprite[17]
            screen.blit(my_image.image, (self.anim_x, my_image.rect.y))
            self.anim_x+=self.num
            if self.anim_x==-8 or self.anim_x==740:
                return 1
            else:
                return 0

        def shoot_cannon(self, time_now):
            duration=0.5
            if self.animate:
                if self.timer == None:
                    self.timer = time_now
                    self.type = round(time_now*10)%3
                different_time=time_now-self.timer 
                if self.type==0:
                    if different_time >= 1.5*duration:
                        self.timer = None
                        self.cannon_sprite[self.cannon_counter].kill()
                        enemies_bullets_nodokill.add(self.cannon_sprite[17])
                        self.cannon_counter = None
                        self.animate = False
                    elif different_time >= 1.2*duration:
                        if self.cannon_counter==16:
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                    elif different_time >= 0.9*duration:
                        if self.cannon_counter==15:
                            if self.isFlip:
                                x = self.cannon_sprite[self.cannon_counter].rect.width/3   
                            else:
                                x = -self.cannon_sprite[self.cannon_counter].rect.width/3 
                            enemies_bullets.add(self.cannon_bullet(damage=10, position_x=self.position_x+x, position_y= self.position_y+self.cannon_sprite[self.cannon_counter].rect.height/2, width=25, height=25, distance=10, type=self.type, isFlip=self.isFlip))  
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1
                            cannonSE.play()
                    elif different_time >= 0.6*duration:
                        if self.cannon_counter==14:  
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1
                    elif different_time >= 0.3*duration:
                        if self.cannon_counter==13:  
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1
                    else:
                        if self.cannon_counter==12:
                            enemies_bullets_nodokill.remove(self.cannon_sprite[17])
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_counter+=1
                        elif self.cannon_counter==None:
                            self.cannon_counter=12
                elif self.type==1:
                    if different_time >= 1.5*duration:
                        self.timer = None
                        self.cannon_sprite[self.cannon_counter].kill()
                        enemies_bullets_nodokill.add(self.cannon_sprite[17])
                        self.cannon_counter = None
                        self.animate = False
                    elif different_time >= 1.2*duration:
                        if self.cannon_counter==11:  
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                    elif different_time >= 0.9*duration:
                        if self.cannon_counter==10:  
                            if self.isFlip:
                                x = self.cannon_sprite[self.cannon_counter].rect.width/2  
                            else:
                                x = -self.cannon_sprite[self.cannon_counter].rect.width/3 
                            enemies_bullets.add(self.cannon_bullet(damage=10, position_x=self.position_x+x, position_y= self.position_y+self.cannon_sprite[self.cannon_counter].rect.height/2, width=25, height=25, distance=10, type=self.type, isFlip=self.isFlip))  
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1
                            cannonSE.play()
                    elif different_time >= 0.6*duration:
                        if self.cannon_counter==9: 
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1
                    elif different_time >= 0.3*duration:
                        if self.cannon_counter==8:
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1  
                    else:
                        if self.cannon_counter==7:
                            enemies_bullets_nodokill.remove(self.cannon_sprite[17])
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_counter+=1
                        elif self.cannon_counter==None:
                            self.cannon_counter=7  
                else:
                    if different_time >= 1.8*duration:
                        self.timer = None
                        self.cannon_sprite[self.cannon_counter].kill()
                        enemies_bullets_nodokill.add(self.cannon_sprite[17])
                        self.cannon_counter = None
                        self.animate = False
                    elif different_time >= 1.5*duration:
                        if self.cannon_counter==5:
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                    elif different_time >= 1.2*duration:
                        if self.cannon_counter==4:
                            if self.isFlip:
                                x = self.cannon_sprite[self.cannon_counter].rect.width/2   
                            else:
                                x = -self.cannon_sprite[self.cannon_counter].rect.width/3 
                            enemies_bullets.add(self.cannon_bullet(damage=10, position_x=self.position_x+x, position_y= self.position_y+self.cannon_sprite[self.cannon_counter].rect.height/2, width=25, height=25, distance=10, type=self.type, isFlip=self.isFlip))  
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1
                            cannonSE.play()
                    elif different_time >= 0.9*duration:
                        if self.cannon_counter==3:
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1   
                    elif different_time >= 0.6*duration:
                        if self.cannon_counter==2:
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1    
                    elif different_time >= 0.3*duration:
                        if self.cannon_counter==1:
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_sprite[self.cannon_counter-1].kill()
                            self.cannon_counter+=1
                    else:
                        if self.cannon_counter==0:
                            enemies_bullets_nodokill.remove(self.cannon_sprite[17])
                            enemies_bullets_nodokill.add(self.cannon_sprite[self.cannon_counter])
                            self.cannon_counter+=1 
                        elif self.cannon_counter==None:
                            self.cannon_counter=0
            else:
                pass
            
class LaserBeam(pygame.sprite.Sprite):
    def __init__(self,*, position_x: int, position_y: int):
        super().__init__()
        self.position_x = position_x
        self.position_y = position_y
        self.timer = None
        data = [
            [2, position_x, position_y-156, 2, 4, 3, False, [0,0]], 
            [3, position_x, position_y-26, 2.5, 5, 3, False, [0,0]],
            [24, position_x, position_y, 2.5, 5, 6, False, [0,0]],
            [27, position_x, position_y, 0.74, 1.48, 6, False, [0,0]],
            [31, position_x, position_y, 0.74, 1.48, 2, False, [0,0]]    
            ] #[quantity: int, position_x: int, position_y: int, widthScale: int, heightScale: int, damage: int, isFlip n: list <x,y>]
        self.laserBeamSprites = make_animsprite(name="asset/laserBeam/ultimateBeam", extension=".png", n=31, data=data)
        data = [
            [3, position_x, position_y, 3.5, 5.5, 0, False, [0,0]],  
            ]
        self.warning = make_animsprite(name="asset/laser_warning", extension=".png", n=3, data=data)
        self.warning_counter = 0
        self.counter = 0
        self.warning_duration = 0
        self.last_warning = 0
        
    def shoot_laser(self, time_now):
        global laser_await
        duration=0.2
        if self.timer == None:
            self.timer = time_now
        different_time=time_now-self.timer
        if different_time >= 28.9*duration:
            self.timer=None
            laser_await = True
            self.laserBeamSprites[self.counter-1].kill()
            self.counter=0
        elif different_time >= 28.6*duration:
            if self.counter==30:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 28.3*duration:
            if self.counter==29:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 28*duration:
            if self.counter==28:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 27.5*duration:
            if self.counter==27:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 27*duration:
            if self.counter==26:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 26*duration:
            if self.counter==25:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 25*duration:
            if self.counter==24:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 24*duration:
            if self.counter==23:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 23*duration:
            if self.counter==22:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 22*duration:
            if self.counter==21:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 21*duration:
            if self.counter==20:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 20*duration:
            if self.counter==19:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 19*duration:
            if self.counter==18:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 18*duration:
            if self.counter==17:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 17*duration:
            if self.counter==16:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 16*duration:
            if self.counter==15:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 15*duration:
            if self.counter==14:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 14*duration:
            if self.counter==13:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 13*duration:
            if self.counter==12:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 12*duration:
            if self.counter==11:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 11*duration:
            if self.counter==10:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 10*duration:
            if self.counter==9:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 9.5*duration:
            if self.counter==8:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 9*duration:
            if self.counter==7:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 8.5*duration:
            if self.counter==6:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 8*duration:
            if self.counter==5:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 7.5*duration:
            if self.counter==4:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 7*duration:
            if self.counter==3:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 6.5*duration:
            if self.counter==2:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.laserBeamSprites[self.counter-1].kill()
                self.counter+=1
        elif different_time >= 6*duration:
            if self.counter==1:
                self.laserBeamSprites[self.counter-1].kill()
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.counter+=1
        elif different_time>= 5.5*duration:
            if self.counter==0:
                enemies_bullets_nodokill.add(self.laserBeamSprites[self.counter])
                self.counter+=1
                laserSE.play()
                #kill all becuase it hard to predict
                self.warning[self.last_warning].kill()
        else:
            mul = 20
            if self.warning_duration<mul*duration:
                if self.warning_counter==0:
                    enemies_bullets_nodokill.add(self.warning[self.warning_counter])
                    self.last_warning=self.warning_counter
                    self.warning_counter+=1
                self.warning_duration+=1
            if self.warning_duration<2*mul*duration:
                if self.warning_counter==1:
                    enemies_bullets_nodokill.add(self.warning[self.warning_counter])
                    self.last_warning=self.warning_counter
                    self.warning[self.warning_counter-1].kill()
                    self.warning_counter+=1
                self.warning_duration+=1
            if self.warning_duration<3*mul*duration:
                if self.warning_counter==2:
                    enemies_bullets_nodokill.add(self.warning[self.warning_counter])
                    self.last_warning=self.warning_counter
                    self.warning_counter-=1
                    self.warning[self.warning_counter].kill()
                self.warning_duration+=1
            elif self.warning_duration<4*mul*duration:
                if self.warning_counter==1:
                    enemies_bullets_nodokill.add(self.warning[self.warning_counter])
                    self.last_warning=self.warning_counter
                    self.warning[self.warning_counter+1].kill()
                    self.warning_counter-=1
                self.warning_duration+=1
            else:
                self.warning_duration=0

def home_page():
    color1 = (255,255,255)
    color_light = (170,170,170)
    color_dark = (100,100,100)

    width = screen.get_width()+300
    height = screen.get_height()

    smallfont = pygame.font.SysFont('Corbel', 35)
    text = smallfont.render('quit', True, color1)
    start_text = smallfont.render('start', True, color1)
    verySmallfont = pygame.font.SysFont('Corbel', 25)
    creators = verySmallfont.render('Created by ThatPersonAyuma', True, (255,255,255))
    while True:
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if width/2 <= mouse[0] <= width/2+800 and height//2 <= mouse[1] <= height/2+600:
                    return "exit"
                elif width/2 <= mouse[0] <= width/2+140 and height//3 <= mouse[1] <= height//3+40:
                    return 1
                
        screen.blit(homebg, (0,0))
        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:  
            pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
            pygame.draw.rect(screen,color_dark,[width/2,height//3,140,40])
        elif width/2 <= mouse[0] <= width/2+140 and height//3 <= mouse[1] <= height//3+40:
            pygame.draw.rect(screen,color_light,[width/2,height//3,140,40]) 
            pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])
        else:  
            pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])    
            pygame.draw.rect(screen,color_dark,[width/2,height//3,140,40])

        screen.blit(text , (width/2+45,height/2))
        screen.blit(start_text , (width/2+41,height//3))
        screen.blit(creators, (500, 570))
        pygame.display.update()


#Only Circle Bullet
def main_screen_1()->list[str,int,int]|str:
    global bullet_wait, isStart, boss_bullet_wait, circle_waiting, laser_await, isCursorActive, playing_time, time_before
    time_before=time.time()
    while (1):
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
        bullets.update()
        enemies_bullets.update()
        enemies_bullets_nodokill.update()
        enemies.update()
        if not isStart:
            pygame.mouse.set_pos((400-player.width/2, 450.0))
            isStart=True
        if isCursorActive:
            x,y = pygame.mouse.get_pos()
            if x<=750 and y<=550:
                    player.rect.x = x
                    player.rect.y = y
            else:
                if x >750:
                    player.rect.x=750
                if y>550:
                    player.rect.y=550
        else:
            pygame.mouse.set_pos((x, y))
        isCursorActive = pygame.mouse.get_focused()
        
        my_time=round(playing_time*10)
        if my_time%(bullet_interval*10)==0 and not bullet_wait:
            bullets.add(player.Bullet(position_x=x+player.width//2, position_y=y, speed=10, damage=bullet_damage))
            bullet_wait = True
            shootSE.play()
        elif my_time%(bullet_interval*10)!=0:
            bullet_wait=False

        if my_time%20==0  and myBoss.health/boss_health<0.9: 
            if not boss_bullet_wait:
                bulletBossSE.play()
                bossBullet=myBoss.BossBullets(damage=20, position_x=x+player.width//2, position_y=35, speed=5, width=26, height=85)
                enemies_bullets.add(bossBullet)
                boss_bullet_wait = True
        elif my_time%20!=0:
            if boss_bullet_wait:
                boss_bullet_wait = False
        if my_time%15==0: 
            if not circle_waiting:                                    #150,180,210,220,240,270,300     #100,120,140,160,140,120,100                        336, 314, 292, 270, 244, 222, 201 | 201, 222, 244, 270, 292, 314, 336
                myBoss.make_circle(group=enemies_bullets, coordinates_x=[180,180,180,180,180], coordinates_y=[100,100,100,100,100], angles = [202, 244, 270, 292, 304], isLeft=True)
                myBoss.make_circle(group=enemies_bullets, coordinates_x=[620,620,620,620,620], coordinates_y=[100,100,100,100,100], angles = [202, 244, 270, 292, 304], isLeft=False)
                circle_waiting = True
        elif my_time%15!=0:
            if circle_waiting:
                circle_waiting = False

        player_hit = pygame.sprite.spritecollide(player, enemies_bullets, False) #kill after contact
        if player_hit:
            for bullet in player_hit:
                if pygame.sprite.collide_mask(player, bullet):
                    player.take_hit(bullet.damage)
                    bullet.kill()
                    if not isPlayerAlive:
                        return "death"
        player_hit_ndk = pygame.sprite.spritecollide(player, enemies_bullets_nodokill, False) #no kill after contact
        if player_hit_ndk:
            for bullet in player_hit_ndk:
                if pygame.sprite.collide_mask(player, bullet):
                    player.take_hit(bullet.damage)
                    if not isPlayerAlive:
                        return "death"
        hit_enemies = pygame.sprite.groupcollide(bullets, enemies, dokilla=0, dokillb=0) #-> dictionary {bullet: list[<enemy>]}
        if hit_enemies:
            for bullet, enemies_presc in hit_enemies.items():
                for enemy in enemies_presc: 
                    if pygame.sprite.collide_mask(bullet, enemy):
                        enemy.take_hit(bullet.damage)
                        bullet.kill()
                        if not isBossAlive:
                            return "win"
                        break
        barBossHealth.fill(color=(255, 0, 0)) 
        barPlayerHealth.fill(color=(170, 255, 0))
        screen.blit(bg, (0,0))
        screen.blit(player.image, (player.rect))
        screen.blit(barBossBg, (200, 50))
        screen.blit(barBossHealth, (220, 55))
        screen.blit(barPlayerBg, (0, 574))
        screen.blit(barPlayerHealth, (5, 577))
        bullets.draw(screen)
        enemies.draw(screen)
        enemies_bullets.draw(screen)
        enemies_bullets_nodokill.draw(screen)
        if myBoss.health/boss_health<0.70:
            val1=left_cannon.cannon_showself(screen=screen)
            val2=right_cannon.cannon_showself(screen=screen)
            if val1 and val2:
                enemies_bullets_nodokill.add(left_cannon.cannon_sprite[17])
                enemies_bullets_nodokill.add(right_cannon.cannon_sprite[17])
                return ["2",x,y]
        keys = pygame.key.get_pressed()
        playing_time+=time.time()-time_before
        if keys[pygame.K_ESCAPE]:
            pygame.image.save(screen, "asset/screen_shoot.jpg")#Screenshoot
            text = pause_screen(x=x,y=y)
            if text:
                restart_stat()
                return "quit"
        time_before = time.time()
        pygame.display.update()

def main_screen_2(x:int, y:int)->list[str,int,int]|str: 
    global bullet_wait, isStart, boss_bullet_wait, circle_waiting, cannon_await, isCursorActive, playing_time, time_before, laser_await
    while (1):
        pygame.time.Clock().tick(60)
        bullets.update()
        enemies_bullets.update()
        enemies_bullets_nodokill.update()
        enemies.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
        x,y = pygame.mouse.get_pos()
        if x<=750 and y<=550:
                player.rect.x = x
                player.rect.y = y
        else:
            if x >750:
                player.rect.x=750
            if y>550:
                player.rect.y=550
        my_time=round(playing_time*10)
        if my_time%(bullet_interval*10)==0 and not bullet_wait:
            bullets.add(player.Bullet(position_x=x+player.width//2, position_y=y, speed=10, damage=bullet_damage))
            bullet_wait = True
            shootSE.play()
        elif my_time%(bullet_interval*10)!=0:
            bullet_wait=False

        if my_time%20==0: 
            if not boss_bullet_wait:
                bulletBossSE.play()
                bossBullet=myBoss.BossBullets(damage=20, position_x=x+player.width//2, position_y=35, speed=5, width=26, height=85)
                enemies_bullets.add(bossBullet)
                boss_bullet_wait = True
        elif my_time%20!=0:
            if boss_bullet_wait:
                boss_bullet_wait = False
        if my_time%15==0 and myBoss.health/boss_health<0.9: 
            if not circle_waiting:                                    #150,180,210,220,240,270,300     #100,120,140,160,140,120,100                        336, 314, 292, 270, 244, 222, 201 | 202, 222, 244, 270, 292, 314, 336
                myBoss.make_circle(group=enemies_bullets, coordinates_x=[180,180,180,180,180,180,180], coordinates_y=[100,100,100,100,100,100,100], angles = [202, 222, 244, 270, 292, 314, 336], isLeft=True)
                myBoss.make_circle(group=enemies_bullets, coordinates_x=[580,580,580,580,580,580,580], coordinates_y=[100,100,100,100,100,100,100], angles = [202, 222, 244, 270, 292, 314, 336], isLeft=False)
                circle_waiting = True
        elif my_time%15!=0:
            if circle_waiting:
                circle_waiting = False
        #both cannon will attack syncro
        if round(playing_time)%5==0 and cannon_await:
            cannon_await = False
            left_cannon.animate = True
            left_cannon.shoot_cannon(time_now=playing_time)
            right_cannon.animate = True
            right_cannon.shoot_cannon(time_now=playing_time)
        elif round(playing_time)%5!=0 and not cannon_await:
            cannon_await = True
        left_cannon.shoot_cannon(time_now=playing_time)
        right_cannon.shoot_cannon(time_now=playing_time)
        
        player_hit = pygame.sprite.spritecollide(player, enemies_bullets, False) #kill after contact
        if player_hit:
            for bullet in player_hit:
                if pygame.sprite.collide_mask(player, bullet):
                    player.take_hit(bullet.damage)
                    bullet.kill()
                    if not isPlayerAlive:
                        return "death"
        player_hit_ndk = pygame.sprite.spritecollide(player, enemies_bullets_nodokill, False) #no kill after contact
        if player_hit_ndk:
            for bullet in player_hit_ndk:
                if pygame.sprite.collide_mask(player, bullet):
                    player.take_hit(bullet.damage)
                    if not isPlayerAlive:
                        return "death"
        hit_enemies = pygame.sprite.groupcollide(bullets, enemies, dokilla=0, dokillb=0) #-> dictionary {bullet: list[<enemy>]}
        if hit_enemies:
            for bullet, enemies_presc in hit_enemies.items():
                for enemy in enemies_presc: 
                    if pygame.sprite.collide_mask(bullet, enemy):
                        enemy.take_hit(bullet.damage)
                        bullet.kill()
                        break
        barBossHealth.fill(color=(255, 0, 0)) 
        barPlayerHealth.fill(color=(170, 255, 0))
        screen.blit(bg, (0,0))
        screen.blit(player.image, (player.rect))
        screen.blit(barBossBg, (200, 50))
        screen.blit(barBossHealth, (220, 55))
        screen.blit(barPlayerBg, (0, 574))
        screen.blit(barPlayerHealth, (5, 577))
        bullets.draw(screen)
        enemies.draw(screen)
        enemies_bullets.draw(screen)
        enemies_bullets_nodokill.draw(screen)
        keys = pygame.key.get_pressed()
        playing_time+=time.time()-time_before
        if keys[pygame.K_ESCAPE]:
            pygame.image.save(screen, "asset/screen_shoot.jpg")#Screenshoot
            text=pause_screen(x=x,y=y)
            if text:
                restart_stat()
                return "quit"
        time_before = time.time()
        pygame.display.update()
        if myBoss.health/boss_health<0.4:
            laser_await = False
            screamSE.play()
            return ["3",x,y]

def main_screen_3(x:int, y:int)->str:
    global bullet_wait, isStart, boss_bullet_wait, circle_waiting, cannon_await, isCursorActive, laser_await, playing_time, time_before
    while (1):
        pygame.time.Clock().tick(60)
        bullets.update()
        enemies_bullets.update()
        enemies_bullets_nodokill.update()
        enemies.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
        x,y = pygame.mouse.get_pos()
        if x<=750 and y<=550:
                player.rect.x = x
                player.rect.y = y
        else:
            if x >750:
                player.rect.x=750
            if y>550:
                player.rect.y=550
        my_time=round(playing_time*10)
        if my_time%(bullet_interval*10)==0 and not bullet_wait:
            bullets.add(player.Bullet(position_x=x, position_y=y, speed=10, damage=bullet_damage))
            bullet_wait = True
        elif my_time%(bullet_interval*10)!=0:
            bullet_wait=False

        if my_time%20==0: 
            if not boss_bullet_wait:
                bulletBossSE.play()
                bossBullet=myBoss.BossBullets(damage=20, position_x=x+player.width//2, position_y=35, speed=5, width=26, height=85)
                enemies_bullets.add(bossBullet)
                boss_bullet_wait = True
        elif my_time%20!=0:
            if boss_bullet_wait:
                boss_bullet_wait = False
        if my_time%12==0 and myBoss.health/boss_health<0.9: 
            if not circle_waiting:                                    #150,180,210,220,240,270,300     #100,120,140,160,140,120,100                        336, 314, 292, 270, 244, 222, 201 | 202, 222, 244, 270, 292, 314, 336
                myBoss.make_circle(group=enemies_bullets, coordinates_x=[180,180,180,180,180,180,180], coordinates_y=[100,100,100,100,100,100,100], angles = [202, 222, 244, 270, 292, 314, 336], isLeft=True)
                myBoss.make_circle(group=enemies_bullets, coordinates_x=[580,580,580,580,580,580,580], coordinates_y=[100,100,100,100,100,100,100], angles = [202, 222, 244, 270, 292, 314, 336], isLeft=False)
                circle_waiting = True
        elif my_time%12!=0:
            if circle_waiting:
                circle_waiting = False

        #both cannon will attack simultaneously
        if round(playing_time)%5==0 and cannon_await:
            cannon_await = False
            left_cannon.animate = True
            left_cannon.shoot_cannon(time_now=playing_time)
            right_cannon.animate = True
            right_cannon.shoot_cannon(time_now=playing_time)
        elif round(playing_time)%5!=0 and not cannon_await:
            cannon_await = True
        left_cannon.shoot_cannon(time_now=playing_time)
        right_cannon.shoot_cannon(time_now=playing_time)
        
        #laser
        if my_time%180==0:
            laser_await=False
        if not laser_await:
            laser.shoot_laser(time_now=playing_time)
        
        player_hit = pygame.sprite.spritecollide(player, enemies_bullets, False) #kill after contact
        if player_hit:
            for bullet in player_hit:
                if pygame.sprite.collide_mask(player, bullet):
                    player.take_hit(bullet.damage)
                    bullet.kill()
                    if not isPlayerAlive:
                        return "death"
        player_hit_ndk = pygame.sprite.spritecollide(player, enemies_bullets_nodokill, False) #no kill after contact
        if player_hit_ndk:
            for bullet in player_hit_ndk:
                if pygame.sprite.collide_mask(player, bullet):
                    player.take_hit(bullet.damage)
                    if not isPlayerAlive:
                        return "death"
        hit_enemies = pygame.sprite.groupcollide(bullets, enemies, dokilla=0, dokillb=0) #-> dictionary {bullet: list[<enemy>]}
        if hit_enemies:
            for bullet, enemies_presc in hit_enemies.items():
                for enemy in enemies_presc: 
                    if pygame.sprite.collide_mask(bullet, enemy):
                        #ara.play()
                        enemy.take_hit(bullet.damage)
                        bullet.kill()
                        if not isBossAlive:
                            return "win"
                        break
        
        barBossHealth.fill(color=(255, 0, 0)) 
        barPlayerHealth.fill(color=(170, 255, 0))
        screen.blit(bg, (0,0))
        screen.blit(player.image, (player.rect))
        screen.blit(barBossBg, (200, 50))
        screen.blit(barBossHealth, (220, 55))
        screen.blit(barPlayerBg, (0, 574))
        screen.blit(barPlayerHealth, (5, 577))
        bullets.draw(screen)
        enemies.draw(screen)
        enemies_bullets.draw(screen)
        enemies_bullets_nodokill.draw(screen)
        keys = pygame.key.get_pressed()
        playing_time+=time.time()-time_before
        if keys[pygame.K_ESCAPE]:
            pygame.image.save(screen, "asset/screen_shoot.jpg")#Screenshoot
            text=pause_screen(x=x,y=y)
            if text:
                restart_stat()
                return "quit"
        time_before = time.time()
        pygame.display.update()

def pause_screen(x:int,y:int)->str:
    pygame.mouse.set_visible(1)
    lowABlack = pygame.Surface((800,600), pygame.SRCALPHA)
    my_background = pygame.image.load("asset/screen_shoot.jpg")
    lowABlack.fill((0,0,0,128))
    text_surfacePause = pygame.font.SysFont('Corbel', 35, True).render("PAUSE", True, (255,255,255))
    text_rectPause = text_surfacePause.get_rect(center=(400, 150))
    text_surfacePA = pygame.font.SysFont('Corbel', 35).render("CONTINUE", True, (0,0,0))
    text_rectPA = text_surfacePA.get_rect(center=(400 , 225))
    text_surfaceQ = pygame.font.SysFont('Corbel', 35).render("QUIT", True, (0,0,0))
    text_rectQ = text_surfaceQ.get_rect(center=(400, 300))
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        colorPA = (0,255,0)
        colorQ = (255,0,0)
        # Cek jika mouse berada di atas tombol
        if text_rectQ.x < mouse[0] < text_rectQ.x + text_rectQ.width and text_rectQ.y < mouse[1] < text_rectQ.y + text_rectQ.height:
            colorQ = (128, 0, 0)
            #pygame.draw.rect(screen, ac, (x, y, text_rect.width, text_rect.height))  # Warna terang saat hover
            if click[0] == 1:
                pygame.mouse.set_pos(x,y)
                pygame.mouse.set_visible(0)
                return 1# return to homepage
        elif text_rectPA.x < mouse[0] < text_rectPA.x + text_rectPA.width and text_rectPA.y < mouse[1] < text_rectPA.y + text_rectPA.height:
            colorPA = (0, 128, 0)
            if click[0] == 1:
                pygame.mouse.set_pos(x,y)
                pygame.mouse.set_visible(0)
                return 0 #play again
            #pygame.draw.rect(screen, ic, (x, y, text_rect.width, text_rect.height))  # Warna normal
        screen.blit(my_background, (0,0))    
        screen.blit(lowABlack, (0,0))
        pygame.draw.rect(screen, colorPA, (text_rectPA.x, text_rectPA.y, text_rectPA.width, text_rectPA.height))
        pygame.draw.rect(screen, colorQ, (text_rectPA.x, text_rectQ.y, text_rectPA.width, text_rectPA.height))
        screen.blit(text_surfacePause, text_rectPause)
        screen.blit(text_surfacePA, text_rectPA)
        screen.blit(text_surfaceQ, text_rectQ)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Win or Lose screen
def win_death_screen(isWin: bool):
    global winText, loseText
    restart_stat()
    text_surfacePA = pygame.font.SysFont('Corbel', 35).render("Play Again", True, (0,0,0))
    text_rectPA = text_surfacePA.get_rect(topleft=(150 , 450))
    text_surfaceQ = pygame.font.SysFont('Corbel', 35).render("Quit", True, (0,0,0))
    text_rectQ = text_surfaceQ.get_rect(topleft=(550 , 450))
    running = True
    if winText==0:
        winText = pygame.transform.scale(pygame.image.load("asset/winText.png"), (800,600)).convert_alpha()
        loseText = pygame.transform.scale(pygame.image.load("asset/loseText.png"), (800, 600)).convert_alpha()
    if isWin:
        screenText = winText
        colorBg = (48,124,255)
        winSE.play()
    else:
        screenText = loseText
        colorBg = (255,255,255)
        loseSE.play()
    while running:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.fill(colorBg)  # Black
        colorPA = (0,255,0)
        colorQ = (255,0,0)
        # Check if the mouse is in the box area
        if text_rectQ.x-40 < mouse[0] < text_rectQ.x-40 + text_rectPA.width and text_rectQ.y < mouse[1] < text_rectQ.y + text_rectPA.height:
            colorQ = (128, 0, 0)
            #pygame.draw.rect(screen, ac, (x, y, text_rect.width, text_rect.height))  # Warna terang saat hover
            if click[0] == 1:
                return "quit"# return to homepage
        elif text_rectPA.x < mouse[0] < text_rectPA.x + text_rectPA.width and text_rectPA.y < mouse[1] < text_rectPA.y + text_rectPA.height:
            colorPA = (0, 128, 0)
            if click[0] == 1:
                return "play" #play again
            #pygame.draw.rect(screen, ic, (x, y, text_rect.width, text_rect.height))  # Warna normal
        pygame.draw.rect(screen, colorPA, (text_rectPA.x, text_rectPA.y, text_rectPA.width, text_rectPA.height))
        pygame.draw.rect(screen, colorQ, (text_rectQ.x-40, text_rectQ.y, text_rectPA.width, text_rectPA.height))
        screen.blit(text_surfacePA, text_rectPA)
        screen.blit(text_surfaceQ, text_rectQ)
        screen.blit(screenText, (0,0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def restart_stat():
    global isBossAlive, isPlayerAlive, barBossHealth, barPlayerHealth, isStart, laser_await
    player.health = player_health
    myBoss.health = boss_health
    enemies.empty()
    bullets.empty()
    enemies_bullets.empty()
    enemies_bullets_nodokill.empty()
    enemies.add(myBoss)
    isBossAlive = True
    isPlayerAlive = True
    barBossHealth=pygame.transform.scale(surface=barBossHealth, size=(360,40))
    barPlayerHealth=pygame.transform.scale(surface=barPlayerHealth, size=(150,20))
    isStart = False
    left_cannon.anim_x=-68
    right_cannon.anim_x=800 
    laser_await = False

def main():
    play_again = False
    while(1):
        if not play_again:
            pygame.mixer.music.play(-1)
            situation = home_page()
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        if situation == 1:
            pygame.mouse.set_visible(0)
            pygame.mixer.music.load(filename="asset/sounds/bg.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            situation = main_screen_1()
            if situation[0] == "2":
                situation = main_screen_2(x=situation[1],y=situation[2])
            if situation[0] == "3":
                situation = main_screen_3(x=situation[1],y=situation[2])
        else:
            pygame.quit()
            break
        pygame.mouse.set_visible(1)
        pygame.mixer.stop()
        pygame.mixer.music.unload()
        if situation == "win":
            situation = win_death_screen(isWin=True) #Win
        elif situation == "death":
            situation = win_death_screen(isWin=False) #Lose
        if situation == "play":
            situation = 1
            play_again = True
            continue
        elif situation == "quit": #Quit to home_screen   
            play_again = False
            pygame.mixer.music.load(filename="asset/sounds/home.mp3")
            pygame.mixer.music.set_volume(0.5)
            continue

#Inizilize
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(8)
pygame.display.set_caption("FIOS", icontitle="title")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.mixer.music.load(filename="asset/sounds/home.mp3")
pygame.mixer.music.set_volume(0.5)
laserSE = pygame.mixer.Sound(file="asset/sounds/laserSound.mp3")
laserSE.set_volume(0.5)
cannonSE = pygame.mixer.Sound(file="asset/sounds/cannon.mp3")
cannonSE.set_volume(0.5)
shootSE = pygame.mixer.Sound(file="asset/sounds/shoot.mp3")
shootSE.set_volume(0.2)
screamSE = pygame.mixer.Sound(file="asset/sounds/scream.mp3")
screamSE.set_volume(2)
winSE = pygame.mixer.Sound(file="asset/sounds/winSound.mp3")
winSE.set_volume(4)
loseSE = pygame.mixer.Sound(file="asset/sounds/loseSound.mp3")
loseSE.set_volume(4)
multipleBulletSE = pygame.mixer.Sound(file="asset/sounds/multipleBulletSE.mp3")
multipleBulletSE.set_volume(0.5)
bulletBossSE = pygame.mixer.Sound(file="asset/sounds/bulletBossSe.mp3")
bulletBossSE.set_volume(1.5)

#DATA FOR MAIN_SCREEN
homebg = pygame.image.load("asset/homebg.jpg")
homebg = pygame.transform.smoothscale(homebg, (800,600)).convert()

#Bg for win or lose
winText = 0
loseText = 0

#Time
playing_time = 0
time_before = 0

#Groups
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies_bullets = pygame.sprite.Group()
enemies_bullets_nodokill = pygame.sprite.Group()   

#Player
player_health=100
player=Player(health=player_health, name="Player")  
isPlayerAlive = True      
bullet_damage = 10

#Set Icon (here because we use player plane image)
pygame.display.set_icon(pygame.transform.scale(surface=player.image, size=(32,32)))

#Background (Remember 800, 600 as width and height)
bg = pygame.image.load("asset/bg.jpg")
bg = pygame.transform.smoothscale(bg, (800,600)).convert()

#Bullets
bullet_wait=False
bullet_interval = 0.5
x, y = 500, 500
isStart = False
isCursorActive = True

barPlayerBg = pygame.surface.Surface(size=(160,26))
barPlayerBg.fill(color=(0,0,0))
barPlayerHealth = pygame.surface.Surface(size=(150,20))

barBossBg = pygame.surface.Surface(size=(400,50))
barBossBg.fill(color=(0,0,0))
barBossHealth = pygame.surface.Surface(size=(360,40))

laser=LaserBeam(position_x=402, position_y=360)
boss_health = 1000
myBoss=Boss(health=boss_health, position_x=400, position_y=63)
enemies.add(myBoss)
isBossAlive = True
boss_bullet_wait = False
circle_waiting = False #circle bullet waiting phase

right_cannon = myBoss.Cannon(position_x=770, position_y=50, widthScale=2, heightScale=2, damage=30)
left_cannon = myBoss.Cannon(position_x=25, position_y=50, widthScale=2, heightScale=2, damage=30, isFlip=True)
cannon_await = True
laser_await = True

#main game
if __name__=="__main__":
    main()