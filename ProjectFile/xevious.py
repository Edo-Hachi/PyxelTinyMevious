import pyxel
import define
import enemy

#------------------------------------------------------------------------------
# グローバル変数
bullet_list = []    #ザッパー管理リスト
enemy_list = []    #敵管理リスト

_VSYNC = 0

#------------------------------------------------------------------------------
# #線形リストオブジェクトへのupdate一括処理
def update_list(list):
    for elem in list:
        elem.update()

#------------------------------------------------------------------------------
#線形リストオブジェクトへのdraw一括処理
def draw_list(list, vsync):
    for elem in list:
        elem.draw(vsync)

#------------------------------------------------------------------------------
#線形リストオブジェクトメンバ破棄
def flash_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
            #print("pop")
        else:
            i += 1

#------------------------------------------------------------------------------
#自弾管理クラス
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = define.BULLET_WIDTH
        self.h = define.BULLET_HEIGHT
        self.alive = True
        
        bullet_list.append(self)
        
    def update(self):
        self.y -= define.BULLET_SPEED
        
        #自弾移動
        if self.y + self.h - 1 < 0:
            self.alive = False
        
        # 自弾と敵とのコリジョン
        i = 0
        j = 0
        bx = 0
        by = 0
        ex = 0
        ey = 0

        bx = self.x
        by = self.y

        while j < len(enemy_list):
            if enemy_list[j].alive == True:

                ex = enemy_list[j].ex
                ey = enemy_list[j].ey

                if ey <= by and by <= (ey + enemy_list[j].eh):
                    if ex <= bx and bx <= (ex + enemy_list[j].ew):
                        #print("HIT! Bltx = "  + str(bx) + " : Blt y = " + str(by))
                        #print("HIT! En_x = "  + str(ex) + " : En_y = " + str(ey))
                        enemy_list[j].alive = False
                        self.alive = False
            
            j += 1

        """        
        while i < len(bullet_list):
            #bx = bullet_list[i].x
            #by = bullet_list[i].y
            bx = self.x
            by = self.y

            while j < len(enemy_list):
                ex = enemy_list[j].ex
                ey = enemy_list[j].ey

                if ey <= by and by <= (ey + enemy_list[j].eh):
                    if ex <= bx and bx <= (ex + enemy_list[j].ew):
                        print("HIT! Bltx = "  + str(bx) + " : Blt y = " + str(by))
                        print("HIT! En_x = "  + str(ex) + " : En_y = " + str(ey))
                j += 1
                #print(j)

            i += 1

            #print(i)
        """

    def draw(self, vsync):

        #print(str(vsync))
        #pyxel.blt(self.x, self.y, 0, 8, 32, 8, 8 , 15)

        
        if vsync % 10:
            pyxel.blt(self.x, self.y, 0, 0, 32, define.BULLET_WIDTH, define.BULLET_HEIGHT, define.MASK_COLOR)
        else:
            pyxel.blt(self.x, self.y, 0, 8, 32, define.BULLET_WIDTH, define.BULLET_HEIGHT, define.MASK_COLOR)

#------------------------------------------------------------------------------
def _Update_Title(self):
    if pyxel.btn(pyxel.KEY_1):
        self.GameState = define.STATE_PLAY
        self.Map_y = (255 - 32)
        self.y_offset = 8
        
        self.px = 128 - 8   #自機の座標
        self.py = 200

        self.vsync = 0

#------------------------------------------------------------------------------
def _Draw_Title(self):
    # 画面を消去
    pyxel.cls(0)
# 1cha = 4pix
    txt = "Smell Like a Tiny XEVIOUS"
    txtlen = len(txt) * 4
    pyxel.text(128 - (txtlen /2), 50, txt, 14)

    txt = "Press [1] to Start Game!"
    txtlen = len(txt) * 4
    pyxel.text(128 - (txtlen /2), 60, txt, 14)
    #pyxel.text(123, 60, txt, 14)

#------------------------------------------------------------------------------
def _Update_Play(self):
        #self.vsync += 1

        if 59 <=  self.vsync:
            self.vsync = 0
        else:
            self.vsync += 1
        #print(str(self.vsync))

        #testcode
        #キー入力＆方向転換
        if pyxel.btn(pyxel.KEY_LEFT):
            self.px  -= define.PLAYER_SPEED
            #self.mDY = 0
            
        if pyxel.btn(pyxel.KEY_RIGHT):            
            self.px += define.PLAYER_SPEED
            #self.mDY = 0
            
        if pyxel.btn(pyxel.KEY_UP):       
            #self.mDX = 0
            self.py -=define.PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_DOWN):
            #self.mDX = 0
            self.py += define.PLAYER_SPEED
        
        #ザッパー発射
        #if pyxel.btn(pyxel.KEY_X):
        if pyxel.btnp(pyxel.KEY_X, 10, 20):
            Bullet(self.px, self.py)
            Bullet(self.px + 10, self.py)
        
        #enemyクラスの共有メンバにプレイヤーの座標をセット
        enemy.Enemy.player_x = self.px
        enemy.Enemy.player_y = self.py

        #敵ダミー発生
        if pyxel.btnp(pyxel.KEY_A, 10, 30):
            #enemy_list.append(enemy.Enemy_Toroid(self.px, self.py, 50, 0))
            enemy_list.append(enemy.Enemy_Toroid(50, 0, 16, 16))


        #自弾更新処理
        update_list(bullet_list)
        flash_list(bullet_list)         
        
        #敵キャラ更新処理
        update_list(enemy_list)
        flash_list(enemy_list)

#------------------------------------------------------------------------------
def _Draw_Play(self):
        # 描画\
        # 画面を消去
        pyxel.cls(0)

        #背景表示
        pyxel.bltm(0,self.y_offset * -1, #実画面の表示原点
                0,   #タイルマップページ番号
                0, self.Map_y , #タイルマップの表示原点
                32,33)   #表示範囲
        
        #self.y_offset -= 0.5
        self.y_offset -= 1
        
        if self.y_offset == 0: 
            self.y_offset = 8
            self.Map_y -= 1
        
        #ソルバルウ
        pyxel.blt(self.px, self.py, 0, 0, 0, define.PLAYER_WIDTH, define.PLAYER_HEIGHT, define.MASK_COLOR)
        
        #レティクル
        pyxel.blt(self.px, self.py - 64, 0, 16, 0, 16, 16, define.MASK_COLOR)

        #線形リストオブジェクトの描画処理
        #if self.vsync % 3 == 0:
        draw_list(bullet_list, self.vsync)  #ザッパー表示

        #敵表示
        draw_list(enemy_list, self.vsync)  #敵表示

        #debug
        temp = "PX= " + str(self.px) + ": PY=" + str(self.py)
        pyxel.text(0, 0, temp, 7)

#------------------------------------------------------------------------------
#ゲームメインループ
class GameMain:

    def __init__(self):
        # 初期化
        pyxel.init(255, 255, caption="Tiny Xevious",
        #                    0         1         2         3         4         5         6         7         8         9         10        11        12        13        14        15
                    palette=[0x000000, 0x8CC323, 0x69B923, 0x007846, 0xF0EB3C, 0x194696, 0x7D7D7D, 0xE61414, 0xFFFFFF, 0x824141, 0xC8AA32, 0x000000, 0x000000, 0x000000, 0xffffff, 0xC896B4],
                    fps = 60,  quit_key=pyxel.KEY_Q)

        #pyxel.init(255, 255, caption="Xevious", fps=60, quit_key=pyxel.KEY_Q)
        pyxel.load("./assets/xevious.pyxres")
        
        pyxel.image(0).load(0, 0, "./assets/xevious_01.png")
        pyxel.image(1).load(0, 0, "./assets/xevious_bg.png")

        self.GameState = define.STATE_TITLE

        pyxel.run(self.update, self.draw)

    def update(self):

        if self.GameState == define.STATE_PLAY:
            _Update_Play(self)
        elif self.GameState == define.STATE_TITLE:
            _Update_Title(self)

    def draw(self):
        if self.GameState == define.STATE_PLAY:
            _Draw_Play(self)
        elif self.GameState == define.STATE_TITLE:
            _Draw_Title(self)

GameMain()
