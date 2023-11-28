import random
import sys
import pygame as pg
import time

start = time.time() #タイマー開始

WIDTH, HEIGHT = 1600, 900

delta = {  # 練習３：押下キーと移動量の辞書
    pg.K_UP: (0, -5),  # キー：移動量／値：（横方向移動量，縦方向移動量）
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect)->tuple[bool,bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    因数 rct:こうかとんor爆弾SurfaceのRect
    戻り値:横方向、縦方向判定結果(画面内:True 画面外:False)
    """

    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return (yoko,tate)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img2 = pg.image.load("ex02/fig/6.png")
    kk_img2 = pg.transform.rotozoom(kk_img2, 0, 2.0)

    kk_rct = kk_img.get_rect()  # 練習３：こうかとんSurfaceのRectを抽出する
    kk_rct.center = 900, 400  # 練習３：こうかとんの初期座標
    bb_img = pg.Surface((20, 20))   # 練習１：透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  # 練習１：黒い部分を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習１：赤い半径10の円を描く
    bb_rct = bb_img.get_rect()  # 練習１：爆弾SurfaceのRectを抽出する
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 練習２：爆弾の速度
    
    #2つめの円
    bb_img2 = pg.Surface((20, 20))   # 透明のSurfaceを作る
    bb_img2.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
    pg.draw.circle(bb_img2, (0, 0, 255), (10, 10), 10)  # 練習１：赤い半径10の円を描く
    bb_rct2 = bb_img2.get_rect()  # 爆弾SurfaceのRectを抽出する
    bb_rct2.centerx = random.randint(0, WIDTH)
    bb_rct2.centery = random.randint(0, HEIGHT)
    vx2, vy2 = +5, +5  # 爆弾の速度


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
            if kk_rct.colliderect(bb_rct):
                print("Game Over")
                return
            
            if kk_rct.colliderect(bb_rct2):
                print("Game Over")
                return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)  # 練習３：こうかとんを移動させる
        
        if not kk_rct.colliderect(bb_rct):
            screen.blit(kk_img, kk_rct)
        else:
            screen.blit(kk_img2, kk_rct) #赤い円にぶつかると画像が変わってゲームオーバー

        if not kk_rct.colliderect(bb_rct2):
            screen.blit(kk_img, kk_rct)
        else:
            screen.blit(kk_img2, kk_rct) #青い円にぶつかると画像が変わってゲームオーバー
            
        bb_rct.move_ip(vx, vy)  # 練習２：爆弾を移動させる
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        bb_rct2.move_ip(vx2, vy2)  # 練習２：爆弾を移動させる
        yoko,tate = check_bound(bb_rct2)
        if not yoko:
            vx2 *= -1
        if not tate:
            vy2 *= -1
        screen.blit(bb_img2, bb_rct2)

        end = time.time() #タイマー終了
        time_diff = end - start  
        print(time_diff) 

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()