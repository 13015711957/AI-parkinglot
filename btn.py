import pygame

class Button():
    def __init__(self,screen,centerxy,width,height,button_color,text_color,msg,size):
        self.screen=screen
        self.width,self.height=width,height
        self.button_color=button_color
        self.text_color=text_color
        self.font=pygame.font.SysFont('SimHei',size)
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.centerx=centerxy[0]-self.width/2+2
        self.rect.centery=centerxy[1]-self.height/2+2
        self.deal_msg(msg)

    def deal_msg(self,msg):
        self.msg_img=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_img_rect=self.msg_img.get_rect()
        self.msg_img_rect.center=self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_img,self.msg_img_rect)