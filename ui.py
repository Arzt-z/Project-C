from ili9XXX import st7789
import lvgl as lv
from machine import Pin
import time

labelBuffer = None
mainboxStyle = None
style_module = None
style_outline = None
labelMainbox = None
colorBuffer = None
colorMain1 = None
colorMain2 = None
colorBG = None
objModuleButton = None
labelmodule = None
obj_buffer = None
oldModuleSelect = None
rows = None
colums = None
nModules = None
currentRow = 0
currentColum = 0
scr=None
oldscr=None
button_sizemenu=None
objMainbox = None

def getCurrentRow():
    global currentRow
    return currentRow

def getCurrentColum():
    global currentColum
    return currentColum

def switchScreen(screenmode):
    global rows
    global colums
    global nModules
    global objModuleButton
    global obj_buffer
    global objMainbox
    count=0
    if screenmode=="menu" :
        for r in range(rows):
            for c in range(colums):
                if count<nModules:
                    objModuleButton[c][r].add_flag(lv.obj.FLAG.HIDDEN)
                    obj_buffer.clear_flag(lv.obj.FLAG.HIDDEN)
                    objMainbox.clear_flag(lv.obj.FLAG.HIDDEN)
                count+=1
        print("loaded")
    else:
        for r in range(rows):
            for c in range(colums):
                if count<nModules:
                    hideMainbox()
                    objModuleButton[c][r].clear_flag(lv.obj.FLAG.HIDDEN)
                count+=1
        print("loaded")

def hideMainbox():
    global obj_buffer
    global objMainbox
    objMainbox.add_flag(lv.obj.FLAG.HIDDEN)
    obj_buffer.add_flag(lv.obj.FLAG.HIDDEN)

def ui_init():
    global scr
    lv.init()
    disp = st7789()
    global colorBuffer
    global colorMainBg
    global colorMainB
    global colorMainB2
    global colorBG
    colorBuffer = lv.color_hex(0x118dfa)
    colorMainBg = lv.color_hex(0xa1c5ff)
    colorMainB = lv.color_hex(0xbed5fa)
    colorMainB2 = lv.color_hex(0x275bb0)
    colorBG = lv.color_hex(0x709Cb3)
    styleOutline()
    #colorBG = lv.color_hex(0x082C63)
    #screen
    scr = lv.scr_act()
    scr.set_style_bg_color(colorBG, lv.PART.MAIN)

def styleOutline():
    global style_outline
    global colorMainB2
    style_outline = lv.style_t()
    style_outline.init()
    style_outline.set_radius(5)
    #style_outline.set_bg_opa(lv.OPA._20)
    style_outline.set_bg_color(lv.palette_lighten(lv.PALETTE.BLUE, 3))
    style_outline.set_outline_width(2)
    style_outline.set_outline_color(lv.palette_main(lv.PALETTE.BLUE))
    style_outline.set_outline_pad(4)

def setoutlineModules(direction):
    global style_outline
    global rows
    global colums
    global oldModuleSelect
    global currentRow
    global currentColum
    
    if oldModuleSelect != None:
        oldModuleSelect.remove_style(style_outline, 0)
        
    if direction == "<LEFT>" or direction =="4":
        currentColum = (currentColum - 1) % colums
    elif direction == "<RIGHT>" or direction =="6":
        currentColum = (currentColum + 1) % colums
    elif direction == "<UP>" or direction =="8":
        currentRow = (currentRow - 1) % rows
    elif direction == "<DOWN>" or direction =="2":
        currentRow = (currentRow + 1) % rows

    objModuleButton[currentColum][currentRow].add_style(style_outline, 0)
    oldModuleSelect = objModuleButton[currentColum][currentRow]
    
def styleModulebuttons(rowsIN, columsIN):
    global rows
    global colums
    global colorMainBg 
    global colorMainB
    global mainboxStyle
    global objModuleButton
    global labelmodule
    global style_module
    global button_sizemenu
    rows = rowsIN
    colums = columsIN
    
    if (int((240/rows)-15)<int((300/colums)-15)):
        button_sizemenu=int((240/rows)-15)
    else:
        button_sizemenu=int((300/colums)-15)
    style_module = lv.style_t()
    style_module.init()
    style_module.set_bg_color(colorMainB)
    #style_buffer.set_border_color(lv.palette_darken(lv.PALETTE.LIGHT_BLUE, 3))
    style_module.set_border_color(colorMainBg)
    style_module.set_border_width(4)
    style_module.set_radius(10)
    style_module.set_shadow_width(10)
    style_module.set_shadow_ofs_y(2)
    style_module.set_shadow_opa(lv.OPA._50)
    style_module.set_text_color(lv.color_white())
    style_module.set_height(button_sizemenu)
    style_module.set_width(button_sizemenu)
    
    
def moduleButtons(rowsIN, columsIN, nModuless):
    global nModules
    global rows
    global colums
    global colorMainBg 
    global colorMainB
    global mainboxStyle
    global objModuleButton
    global labelmodule
    global style_module
    global button_sizemenu
    global scr
    rows = rowsIN
    colums = columsIN
    nModules = nModuless
    count = 0
    objModuleButton = [[lv.obj(scr) for _ in range(rows)] for _ in range(colums)]
    labelmodule = [[lv.label(objModuleButton) for _ in range(rows)] for _ in range(colums)]
    for r in range(rows):
        for c in range(colums):
            if count<nModules:
                objModuleButton[c][r].add_style(style_module, 0)
                labelmodule[c][r] = lv.label(objModuleButton[c][r])
                labelmodule[c][r].set_style_text_color(lv.color_hex(0x00040B), lv.PART.MAIN)
                #objModuleButton[c][r].set_pos(((button_size+15)*c)+int((300-((button_size+15)*colums))/2)+15,int(7+240/rows * r))
                objModuleButton[c][r].set_pos(((button_sizemenu+15)*c)+int((300-((button_sizemenu+15)*colums))/2)+15,((button_sizemenu+15)*r)+int((240-((button_sizemenu+15)*rows))/2)+5)
                labelmodule[c][r].align(lv.ALIGN.CENTER, 0, 0)
                labelmodule[c][r].set_text(str(c)+ "," + str(r))
                                
            else:
                objModuleButton[c][r].delete()
            count+=1;

def moduleButtonstext(c,r,text):
    global labelmodule 
    labelmodule[c][r].set_text(text)

def buffer():
    global labelBuffer
    global colorBuffer
    global obj_buffer
    style_buffer = lv.style_t()
    style_buffer.init()
    style_buffer.set_bg_color(colorBuffer)
    #style_buffer.set_border_color(lv.palette_darken(lv.PALETTE.LIGHT_BLUE, 3))
    style_buffer.set_border_width(0)
    style_buffer.set_radius(10)
    style_buffer.set_shadow_width(10)
    style_buffer.set_shadow_ofs_y(2)
    style_buffer.set_shadow_opa(lv.OPA._50)
    style_buffer.set_text_color(lv.color_white())
    style_buffer.set_width(290)
    style_buffer.set_height(30)
    
    obj_buffer = lv.obj(lv.scr_act())
    obj_buffer.add_style(style_buffer, 0)
    obj_buffer.align(lv.ALIGN.TOP_MID, 0, 8)
    labelBuffer = lv.label(obj_buffer)
    labelBuffer.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
    labelBuffer.align(lv.ALIGN.LEFT_MID, 0, 0)
    labelBuffer.set_text("")

def buffer_update(buffer):
    global labelBuffer
    labelBuffer.set_text(buffer)


def mainbox():
    global mainboxStyle
    global labelMainbox
    global objMainbox
    objMainbox = lv.obj(lv.scr_act())
    labelMainbox = lv.label(objMainbox)
    labelMainbox.set_text("")
    labelMainbox.set_style_text_color(lv.color_hex(0x00040B), lv.PART.MAIN)
    objMainbox.add_style(mainboxStyle, 0)
    objMainbox.align(lv.ALIGN.CENTER, 0, 20)
    
def mainbox_update(result):
    global labelMainbox
    labelMainbox.set_text(result)


def mainbox_style():
    global mainboxStyle
    global colorMainBg 
    global colorMainB
    mainboxStyle = lv.style_t()
    mainboxStyle.init()
    mainboxStyle.set_bg_color(colorMainBg )
    mainboxStyle.set_border_color(colorMainB)
    mainboxStyle.set_border_width(4)
    mainboxStyle.set_radius(10)
    mainboxStyle.set_shadow_width(5)
    mainboxStyle.set_shadow_ofs_y(2)
    mainboxStyle.set_shadow_opa(lv.OPA._50)
    mainboxStyle.set_text_color(lv.color_white())
    mainboxStyle.set_width(300)
    mainboxStyle.set_height(190)
