import pyxel
import define
import enemy

bullet_list = []    #ザッパー管理リスト

# グローバル変数
#_VSYNC = 0

enemy_list = []    #敵管理リスト

# #線形リストオブジェクトへのupdate一括処理
def update_list(list):
    for elem in list:
        elem.update()

#線形リストオブジェクトへのdraw一括処理
def draw_list(list, vsync):
    for elem in list:
        elem.draw(vsync)
        

#線形リストオブジェクト        
def flash_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
            #print("pop")
        else:
            i += 1


#ザッパー管理クラス
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
        
        if self.y + self.h - 1 < 0:
            self.alive = False
            
    def draw(self, vsync):

        #print(str(vsync))
        #pyxel.blt(self.x, self.y, 0, 8, 32, 8, 8 , 15)

        
        if vsync % 10:
            pyxel.blt(self.x, self.y, 0, 0, 32, 8, 8 , 15)
        else:
            pyxel.blt(self.x, self.y, 0, 8, 32, 8, 8 , 15)
        


class Gump_main:
    

    def __init__(self):
        # 初期化


        pyxel.init(255, 255, caption="Xevious",
        #                    0         1         2         3         4         5         6         7         8         9         10        11        12        13        14        15
                    palette=[0x000000, 0x8CC323, 0x69B923, 0x007846, 0xF0EB3C, 0x194696, 0x7D7D7D, 0xE61414, 0xFFFFFF, 0x824141, 0xC8AA32, 0x000000, 0x000000, 0x000000, 0x000000, 0xC896B4],
                    fps = 60,  quit_key=pyxel.KEY_Q)

        #pyxel.init(255, 255, caption="Xevious", fps=60, quit_key=pyxel.KEY_Q)
        pyxel.load("./assets/xevious.pyxres")
        
        pyxel.image(0).load(0, 0, "./assets/xevious_01.png")
        pyxel.image(1).load(0, 0, "./assets/xevious_bg.png")

        self.Map_y = (255 - 32)
        self.y_offset = 8
        
        self.px = 100   #自機の座標
        self.py = 100

        self.vsync = 0

        # 実行
        pyxel.run(self.update, self.draw)

    def update(self):

        self.vsync += 1

        if 59 <=  self.vsync:
            self.vsync = 0
        else:
            self.vsync += 1
        #print(str(self.vsync))

        #testcode
        #キー入力＆方向転換
        if pyxel.btn(pyxel.KEY_LEFT):
            self.px  -= 2
            #self.mDY = 0
            
        if pyxel.btn(pyxel.KEY_RIGHT):            
            self.px += 2
            #self.mDY = 0
            
        if pyxel.btn(pyxel.KEY_UP):       
            #self.mDX = 0
            self.py -=2

        if pyxel.btn(pyxel.KEY_DOWN):
            #self.mDX = 0
            self.py += 2
        
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
            enemy_list.append(enemy.Enemy_Toroid(self.px, self.py, 50, 0))


        #自弾更新処理
        update_list(bullet_list)
        flash_list(bullet_list)         
        
        #敵キャラ更新処理
        update_list(enemy_list)
        flash_list(enemy_list)


    def draw(self):
        # 描画
        # 画面を消去
        pyxel.cls(0)
        
        #pyxel.tilemap(0).refimg = 1
        
        #pyxel.tilemap(0).copy(0, 0, 0, 16, 16, 0, 0)
        
        #pyxel.rect(0,0,100,100, 1)

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
        pyxel.blt(self.px, self.py, 0, 0, 0, 16, 16, define.MASK_COLOR)
        
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



Gump_main()
