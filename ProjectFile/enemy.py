import pyxel
import random
import define


class Enemy:

    #プレイヤーの座標（クラス内共有）
    player_x = 0
    player_y = 0

    def __init__(self, _px, _py, _ex, _ey):
        if _px <= 128:
            self.ex = 128 + random.randint(0, 100)
        else:
            self.ex = 128 - random.randint(0, 100)
        
        #self.ex = _ex
        self.ey = 0

        temp = random.randint(0, 2) 
        if temp == 0:
            self.vx = 1
        elif temp == 1:
            self.vx = -1
        else:
            self.vx = 0
        
        #移動速度
        self.vspd = 1

        self.alive = True

        #アクション開始Y座標
        self.act_y = _py - 60
        #enemy_list.append(self)

#トーロイド型の敵
class Enemy_Toroid(Enemy):
    def update(self):
        self.ey += 2

        #アクション開始座標に到達してるか？
        if(self.act_y < self.ey):
            #if(self.px)
            self.vspd += 0.5
            if self.ex < self.player_x:
                self.vx = -1
            else:
                self.vx = 1

        self.ex += self.vx * self.vspd

        #debug
        print(str(self.player_x) + ":" + str(self.player_y))


        #画面外に出たら削除
        if self.ey <= -16:
            self.alive = False
        if 256 <= self.ey:
            self.alive = False

    def draw(self, vsync):
        PAGE = 0
        #MASK_COL = 15

        #pyxel.blt(self.ex, self.ey, 0, 0, 32, 32, 32)
        pyxel.blt(self.ex, self.ey, PAGE, 0, 16, 16, 16, define.MASK_COLOR)

