import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))
dic_mv = {#押下キーと移動量の辞書
        pg.K_UP:(0, -5),
        pg.K_DOWN:(0, +5),
        pg.K_LEFT:(-5, 0),
        pg.K_RIGHT:(+5, 0)}


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect,または爆弾Rectの画面外判定用の関数
    引数：こうかとんRect,または爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果（True:画面内，False:画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #こうかとんの設定
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    #爆弾の設定
    bom_img = pg.Surface((20, 20))
    bom_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bom_img,(255, 0, 0), (10, 10), 10)
    bom_rct = bom_img.get_rect()
    bom_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx,vy = +5, +5


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bom_rct): # こうかとんと爆弾がぶつかったら
            print("Game Over")
            return
        screen.blit(bg_img, [0, 0]) 

        #こうかとんの移動と表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in dic_mv.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        #爆弾の移動と表示
        bom_rct.move_ip(vx,vy)
        screen.blit(bom_img, bom_rct)
        yoko, tate = check_bound(bom_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
