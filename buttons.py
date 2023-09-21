import pygame
from colors import *
from settings import *

def createButton(screen, font, x, y, w, h, txt = ""):
    btn_rect = pygame.rect.Rect((x, y, w, h))
    mouse_pos = pygame.mouse.get_pos()
    hovered = btn_rect.collidepoint(mouse_pos)
    btn_color = BTN_COL
    btn_outline = BTN_H_COL
    if(hovered):
        btn_color = BTN_H_COL
        btn_outline = BTN_COL

    
    pygame.draw.rect(screen, btn_color, btn_rect, 0, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED)
    pygame.draw.rect(screen, btn_outline, btn_rect, 5, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED)
    txt_surface = font.render(txt, False, white)
    txt_rect = txt_surface.get_rect(center = btn_rect.center)
    screen.blit(txt_surface, txt_rect)
    
    if(pygame.mouse.get_pressed()[MOUSE_BTN_1]):
        if(hovered):
            return True
    return False