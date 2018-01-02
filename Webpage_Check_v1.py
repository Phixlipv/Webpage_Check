## -*- coding: utf-8 -*-
import pygame, sys, urllib, Send_Email
from pygame.locals import *

#---Global Preset---#
Screen_Width=400
Screen_Height=300

#Color:
Black=(0,0,0)
White=(255,255,255)
Grey1=(150,150,150)

Display_surface = pygame.display.set_mode((Screen_Width, Screen_Height),RESIZABLE)
#---Global Preset---#

Running=False
Mouse_Pressed=False
Mouse_Is_Pressing=False

#---Timer_Write() Preset---#
Time=[0,0,0]
Clear_Time=False
Minute_Spent=0
Hour_Spent=0
Time_Spent=0
Millisecond_Part=0
Clear_Time_Count=0
#---Timer_Write() Preset---#

Last_Time = 0
Last_Web_content = 'Something'

Hour_T = '00'
Minute_T = '00'
Second_T = '00'

textRectWidth = 0

def main():

    pygame.init()
    pygame.display.set_caption('Philip\'s Timer')

    while True:

        Display_surface.fill(Black)
        Pause_Start_Button()
        Timer_Write()
        Automatic_Web_Check()
        
        pygame.display.flip()

        Get_All_Events()

def Pause_Start_Button():
    global Screen_Width,Screen_Height,Running
    Button_Width=100
    Button_Height=60
    Button_PosX=Screen_Width/2-Button_Width/2
    Button_PosY=Screen_Height-70
    Button_Rect=pygame.draw.rect(Display_surface,Grey1,(Button_PosX,Button_PosY,Button_Width,Button_Height))
    Mouse_X,Mouse_Y=pygame.mouse.get_pos()

    if Button_Rect.collidepoint(Mouse_X,Mouse_Y) and Running==False:
        if pygame.mouse.get_pressed()[0]:
            Write_Words('Start',Button_PosX+Button_Width/2,Button_PosY+Button_Height/2,15,Black)
        else:
            Button_Rect=pygame.draw.rect(Display_surface,Grey1,(Button_PosX-2,Button_PosY-2,Button_Width+4,Button_Height+4))
            Write_Words('Start',Button_PosX+Button_Width/2,Button_PosY+Button_Height/2,15,Black)
        if Mouse_Clicked_Release():
            Running=True
    elif Running:
        Write_Words('Pause',Button_PosX+Button_Width/2,Button_PosY+Button_Height/2,15,Black)
        if Button_Rect.collidepoint(Mouse_X,Mouse_Y):
            if pygame.mouse.get_pressed()[0]:
                Write_Words('Pause',Button_PosX+Button_Width/2,Button_PosY+Button_Height/2,15,Black)
            else:
                Button_Rect=pygame.draw.rect(Display_surface,Grey1,(Button_PosX-2,Button_PosY-2,Button_Width+4,Button_Height+4))
                Write_Words('Pause',Button_PosX+Button_Width/2,Button_PosY+Button_Height/2,15,Black)
            if Mouse_Clicked_Release():
                Running=False
    elif Running==False:
        Write_Words('Start',Button_PosX+Button_Width/2,Button_PosY+Button_Height/2,15,Black)


def Write_Words(string,center_x,center_y,font_size,text_color):
    global Black,White
    font_1 = pygame.font.SysFont('simhei', font_size)
    textSurfaceObj = font_1.render('%s'%(string), True, text_color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (center_x,center_y)     
    Display_surface.blit(textSurfaceObj, textRectObj)

def Write_Words_GetWidth(string,font_size):
    global textRectWidth
    font_1 = pygame.font.SysFont('simhei', font_size)
    textSurfaceObj = font_1.render('%s'%(string), True, Black)
    textRectObj = textSurfaceObj.get_rect()
    textRectWidth = textSurfaceObj.get_size()[0]
    textRectObj.center = (0,0)
    return textSurfaceObj.get_size()[0]


def Mouse_Clicked_Release():
    global Mouse_Is_Pressing
    if pygame.mouse.get_pressed()[0]:
        Mouse_Is_Pressing=True
    if pygame.mouse.get_pressed()[0]==False and Mouse_Is_Pressing==True:
        Mouse_Is_Pressing=False
        return True
    else:
        return False


def Timer_Write():
    global Time,Screen_Width,Screen_Height,Running,Minute_Spent,Hour_Spent,Time_Spent,Millisecond_Part,Clear_Time,Clear_Time_Count, Hour_T, Minute_T, Second_T, textRectWidth

    Second_Spent_Display=0

    Write_Words('%s:%s:%s'%(Hour_T,Minute_T,Second_T),Screen_Width/2,Screen_Height/2,Screen_Width/10,White)
    Write_Words_GetWidth('%s:%s:%s'%(Hour_T,Minute_T,Second_T),Screen_Width/10)

    MDistance = Screen_Width/2 + Write_Words_GetWidth('%s:%s:%s'%(Hour_T,Minute_T,Second_T),Screen_Width/10)/2 + Write_Words_GetWidth('000',textRectWidth/4)/2

    if Running:
        Clear_Time=False
        Time_Spent=pygame.time.get_ticks()-Clear_Time_Count
        Millisecond_Part=str(Time_Spent)[len(str(Time_Spent))-3:len(str(Time_Spent))]
        Write_Words('.'+Millisecond_Part, MDistance, Screen_Height/2,textRectWidth/4,Grey1)
        if len(str(Time_Spent))>=4:
            Second_Spent_Display=int(str(Time_Spent)[0:int(len(str(Time_Spent)))-3])-60*Minute_Spent
            if Second_Spent_Display==60:
                Minute_Spent+=1
        Minute_Spent_Display=Time_Spent/60000-60*Hour_Spent
        if Minute_Spent_Display==60:
            Hour_Spent+=1
        Hour_Spent_Display=Time_Spent/3600000
        Time[2]=Second_Spent_Display
        Time[1]=Minute_Spent_Display
        Time[0]=Hour_Spent_Display

    elif Running==False:
        if Millisecond_Part==0:
            Write_Words('.000',MDistance,Screen_Height/2,textRectWidth/4,Grey1)
        else:
            Write_Words('.'+str(Millisecond_Part),MDistance,Screen_Height/2,textRectWidth/4,Grey1)

        if Clear_Time==True:
            Clear_Time_Count=pygame.time.get_ticks()
        else:
            Clear_Time_Count=pygame.time.get_ticks()-Time_Spent
        
    if Reset_Button_and_CheckReset():
        Running=False
        Minute_Spent=0
        Hour_Spent=0
        Time=[0,0,0]
        Millisecond_Part='000'
        Clear_Time=True

    if Time[0]<10:
        Hour_T = '0'+str(Time[0])
    else:
        Hour_T = str(Time[0])
    if Time[1]<10:
        Minute_T = '0'+str(Time[1])
    else:
        Minute_T = str(Time[1])
    if Time[2]<10:
        Second_T = '0'+str(Time[2])
    else:
        Second_T = str(Time[2])

def Automatic_Web_Check():
    global Last_Time, Last_Web_content
    URL_site = 'http://www.imperial.ac.uk/study/campus-life/accommodation/halls/returning-students-accommodation/'

##    if Last_Time!=Time[1]:
##        Last_Time=Time[1]
##        Web_open = urllib.urlopen(URL_site)
##        Web_content = Web_open.read()
##        if Last_Web_content!=Web_content:
##            print 'Content has been changed'
##        else:
##            print 'No update'

    if Last_Time!=Time[2] and Time[2]%10==0:
        Last_Time=Time[2]
        
        Web_open = urllib.urlopen(URL_site)
        Web_content = Web_open.read()
        if Last_Web_content!=Web_content:
            print 'Content has been changed'
            Send_Email.main()
            Last_Web_content=Web_content
        else:
            print 'No update'


def Reset_Button_and_CheckReset():
    Button_Rect_PosX=50
    Button_Rect_PosY=50
    Button_Rect_Width=50
    Button_Rect_Height=30
    Mouse_X,Mouse_Y=pygame.mouse.get_pos()
    Button_Rect=pygame.draw.rect(Display_surface,Grey1,(Button_Rect_PosX,Button_Rect_PosY,Button_Rect_Width,Button_Rect_Height))
    
    if Button_Rect.collidepoint(Mouse_X,Mouse_Y):
        if pygame.mouse.get_pressed()[0]:
            Write_Words('Reset',Button_Rect_PosX+Button_Rect_Width/2,Button_Rect_PosY+Button_Rect_Height/2,12,Black)
        else:
            Button_Rect=pygame.draw.rect(Display_surface,Grey1,(Button_Rect_PosX-1,Button_Rect_PosY-1,Button_Rect_Width+2,Button_Rect_Height+2))
            Write_Words('Reset',Button_Rect_PosX+Button_Rect_Width/2,Button_Rect_PosY+Button_Rect_Height/2,12,Black)
        if Mouse_Clicked_Release():
            return True
    else:
        Write_Words('Reset',Button_Rect_PosX+Button_Rect_Width/2,Button_Rect_PosY+Button_Rect_Height/2,12,Black)
        return False


def Get_All_Events():
    global Screen_Width, Screen_Height
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==VIDEORESIZE:
            Display_surface=pygame.display.set_mode(event.dict['size'],RESIZABLE)
            pygame.display.flip()
            Screen_Width = event.dict['size'][0]
            Screen_Height = event.dict['size'][1]
    
        
if __name__ == '__main__':
    main()
