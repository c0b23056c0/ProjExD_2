import os
import random
import sys
import time
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


def kk_rt(img, idouryou):
    """
    こうかとんの回転角度計算用の関数
    引数：kk_imgと移動量のタプル
    戻り値：移動量の合計値タプルのキーとrotozoomしたSurfaceを値とした辞書
    """
    if idouryou == (-5, 0):
        return {idouryou:pg.transform.rotozoom(img, 0, 1.0)}
    if idouryou == (-5, +5):
        return {idouryou:pg.transform.rotozoom(img, 45, 1.0)}
    if idouryou == (-5, -5):
        return {idouryou:pg.transform.rotozoom(img, 315, 1.0)}
    if idouryou == (0, +5):
        pg.transform.flip(img, True, False)
        return {idouryou:pg.transform.rotozoom(img, 90, 1.0)}
    if idouryou == (+5, +5):
        pg.transform.flip(img, True, False)
        return {idouryou:pg.transform.rotozoom(img, 45, 1.0)}
    if idouryou == (0,-5):
        pg.transform.flip(img, True, False)
        return {idouryou:pg.transform.rotozoom(img, 270, 1.0)}
    if idouryou == (+5, -5):
        pg.transform.flip(img, True, False)
        return {idouryou:pg.transform.rotozoom(img, 315, 1.0)}
    if idouryou == (+5, 0):
        return {idouryou:pg.transform.rotozoom(img, 0, 1.0)}


def gameover(screen):
    go_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_img,(0,0, 0), (0, 0, WIDTH, HEIGHT), width = 0)
    go_rct = go_img.get_rect()
    go_img.set_alpha(200)
    screen.blit(go_img, go_rct)
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    screen.blit(txt,[600, 400])
    koka_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    koka_rct = koka_img.get_rect()
    koka_rct.center = 500, 450
    screen.blit(koka_img, koka_rct)
    koka_rct.center = 1100, 450
    screen.blit(koka_img, koka_rct)
    pg.display.update()
    time.sleep(5)



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
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        #こうかとんの移動と表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        kk_new_img = pg.transform.rotozoom(kk_img, 0, 1.0)
        for k,v in dic_mv.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                new_v = (v[0], v[1])
                print(new_v)
                dic_rtz = kk_rt(kk_img,new_v)
                kk_new_img = dic_rtz[new_v]
                print(dic_rtz)
            """
            pi = kk_rt(k)
            print(pi)
            kk_img = pg.transform.rotate(kk_img, pi)
            """
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_new_img, kk_rct)
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
