import pyxel

class App:
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

        self.Map_y = (128 - 32)
        self.y_offset = 8
        
        self.px = 100
        self.py = 100

        # 実行
        pyxel.run(self.update, self.draw)

    def update(self):
        # 更新
        
        #self.Map_y -= 1
        
        #self.y_offset = 8
        
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
        
    def draw(self):
        # 描画
        # 画面を消去
        pyxel.cls(0)
        
        #pyxel.tilemap(0).refimg = 1
        
        #pyxel.tilemap(0).copy(0, 0, 0, 16, 16, 0, 0)
        
        #pyxel.rect(0,0,100,100, 1)

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
        pyxel.blt(self.px, self.py, 0, 0, 0, 16, 16, 15)
        
        #レティクル
        pyxel.blt(self.px, self.py - 64, 0, 16, 0, 16, 16, 15)

App()
