#! /home/pi/lv_micropython/ports/unix/micropython

import usys as sys
sys.path.append('') # See: https://github.com/micropython/micropython/issues/6419

# try:
#     script_path = __file__[:__file__.rfind('/')] if __file__.find('/') >= 0 else '.'
# except NameError:
#     script_path = ''
import lvgl as lv
lv.init()
import SDL,time,uos
SDL.init()
import fs_driver
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')

# Register SDL display driver.

draw_buf = lv.disp_draw_buf_t()
buf1_1 = bytearray(1280*5)
draw_buf.init(buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = draw_buf
disp_drv.flush_cb = SDL.monitor_flush
disp_drv.hor_res = 1280
disp_drv.ver_res = 720
disp_drv.register()
# Regsiter SDL mouse driver

indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = SDL.mouse_read
indev_drv.register()

#font
myfont_jp = lv.font_load("S:/home/pi/gpsnavi/font/font-jp-48.bin")
myfont_jp_60 = lv.font_load("S:/home/pi/gpsnavi/font/font-jp-60.bin")
#myfont_jp = lv.font_load("S:%s/font-PHT-jp-48.bin" % script_path)
#
# A simple meter
#
meter = lv.meter(lv.scr_act())
meter.center()
meter.set_size(650,650)

# Add a scale first
scale = meter.add_scale()
meter.set_scale_ticks(scale, 51, 2, 10, lv.palette_main(lv.PALETTE.GREY))
#meter.set_scale_major_ticks(scale, 10, 4, 15, lv.color_black(), 10)

indic = lv.meter_indicator_t()

# Add a blue arc to the start
indic = meter.add_arc(scale, 3, lv.palette_main(lv.PALETTE.BLUE), 0)
meter.set_indicator_start_value(indic, 0)
meter.set_indicator_end_value(indic, 50)

# Make the tick lines blue at the start of the scale
indic = meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
meter.set_indicator_start_value(indic, 0)
meter.set_indicator_end_value(indic, 50)

# Add a red arc to the end
indic = meter.add_arc(scale, 3, lv.palette_main(lv.PALETTE.RED), 0)
meter.set_indicator_start_value(indic, 50)
meter.set_indicator_end_value(indic, 100)

# Make the tick lines red at the end of the scale
indic = meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
meter.set_indicator_start_value(indic, 50)
meter.set_indicator_end_value(indic, 100)

# Add a needle line indicator
indic = meter.add_needle_line(scale, 18, lv.palette_main(lv.PALETTE.GREEN), -10)


#
# Using the Size, Position and Padding style properties
#
style = lv.style_t()
style.init()
style.set_radius(5)
# Make a gradient
style.set_width(300)
style.set_height(lv.SIZE.CONTENT)

#300 
style1 = lv.style_t()
style1.init()
style1.set_radius(50)
style1.set_width(300)
style1.set_border_color(lv.color_hex(0xF0F0F0))
style1.set_height(80)
#100
style2 = lv.style_t()
style2.init()
style2.set_radius(5)
style2.set_width(100)
style2.set_height(lv.SIZE.CONTENT)
style2.set_border_color(lv.color_hex(0xFFFFFF))
style2.set_text_color(lv.palette_main(lv.PALETTE.BLUE))
#630
style3 = lv.style_t()
style3.init()
style3.set_radius(5)
style3.set_width(630)
style3.set_height(lv.SIZE.CONTENT)
#350
style4 = lv.style_t()
style4.init()
style4.set_radius(5)
style4.set_width(350)
style4.set_height(lv.SIZE.CONTENT)

# nav
txt1 = lv.obj(lv.scr_act())
txt1.add_style(style1, 0)
txt1.center() 
label1 = lv.label(txt1)
label1.center()
label1.set_style_text_font(myfont_jp_60, 0)  # set the font
label1.set_text("Wait.. ")
#工程
txt2 = lv.obj(lv.scr_act())
txt2.add_style(style4, 0)
txt2.set_pos(10, 10)  
label2 = lv.label(txt2)
label2.set_style_text_font(myfont_jp, 0)  # set the font
#幅
txt3 = lv.obj(lv.scr_act())
txt3.add_style(style, 0)
txt3.set_pos(10, 210)  
label3 = lv.label(txt3)
label3.set_style_text_font(myfont_jp, 0)  # set the font

# txt4 = lv.obj(lv.scr_act())
# txt4.add_style(style, 0)
# txt4.set_pos(10, 310)  
# label4 = lv.label(txt4)
# label4.set_style_text_font(myfont_jp, 0)  # set the font
#offset
txt5 = lv.obj(lv.scr_act())
txt5.add_style(style4, 0)
txt5.set_pos(10, 510)  
label5 = lv.label(txt5)
label5.set_style_text_font(myfont_jp, 0)  # set the font
#圃場面積
txt6 = lv.obj(lv.scr_act())
txt6.add_style(style3, 0)
txt6.set_pos(10, 610)  
label6 = lv.label(txt6)
label6.set_style_text_font(myfont_jp, 0)  # set the font
#作業面積
txt7 = lv.obj(lv.scr_act())
txt7.add_style(style3, 0)
txt7.set_pos(640, 610)  
label7 = lv.label(txt7)
label7.set_style_text_font(myfont_jp, 0)  # set the font
#基準線
txt8 = lv.obj(lv.scr_act())
txt8.add_style(style2, 0)
txt8.set_pos(600, 430)  
label8 = lv.label(txt8)
label8.set_style_text_font(myfont_jp_60, 0)  # set the font
# #速度
# txt9 = lv.obj(lv.scr_act())
# txt9.add_style(style3, 0)
# txt9.set_pos(900, 10)  
# label9 = lv.label(txt9)
# label9.set_style_text_font(myfont_jp, 0)  # set the font

import socket
from struct import unpack


keyname=["0","A","B","C","S","W","D","View","Rain","EX","Half","M2","SHP"]
blf = False
view =False
oldmsg=[0,0,0,0,0,0,-1,-1,-1,0]
delta=[0,0,0,0,0,0,0,0,0,0]
addr = socket.getaddrinfo('0.0.0.0', 50001)[0][-1]
print(addr)
s = socket.socket()
s.bind(addr)
s.listen(2)

print('listening on', addr)
cl, addr = s.accept()
print('client connected from', addr)
while True:

    buff = cl.recv(40)
    # print(cl)
    # print(len(buff))
    if buff:
        newmsg=unpack('10i',buff)
        # print(newmsg)
        for i in range(10):
            if (newmsg[i] == oldmsg[i]):
                delta[i]=False
            else :
                delta[i]=True
        #     print(delta[i])

        # print(delta)

        meter.set_indicator_value(indic, int(newmsg[0])+50)
        if newmsg[0] < 0:
            style1.set_text_color(lv.palette_darken(lv.PALETTE.BLUE, 4))
        elif newmsg[0] > 0:
            style1.set_text_color(lv.palette_darken(lv.PALETTE.RED, 4))
        else:
            style1.set_text_color(lv.palette_darken(lv.PALETTE.GREEN, 4))

        if newmsg[9] == 0:
            if delta[1]:
                label1.set_text("  %+4d ㎝"%newmsg[1])
            if delta[2]:
                label2.set_text("工程 :%d" %newmsg[2])
            if delta[3]:
                label3.set_text("幅 :%d㎝" %newmsg[3])
            # label4.set_text("rev :%d" %newmsg[4])
            if delta[4]:
                label5.set_text("offset :%d㎝" %newmsg[5])
            if delta[6]:
                label6.set_text("圃場面積 :%4d㎡" %newmsg[6])
            if delta[7]:
                label7.set_text("作業面積 :%4d㎡" %newmsg[7])
            
            if blf==False :
                label8.set_text("→" ) 
            elif blf==True:
                label8.set_text("←" ) 
            #label9.set_text("速度 :%.2fm/s" %navidata[10])
        else:
            key=newmsg[9]
            # print(key)
            label1.set_text("%s pressed"%keyname[key])
            time.sleep(1)
            if key == 6:
                blf = not(blf)
            elif key == 7:
                view = not(view)
                if view:
                    uos.system('wmctrl -a "sudo"' )
                else :
                    uos.system('wmctrl -a "TFT Simulator"' )
        oldmsg = newmsg
            
        # print(str(data, 'utf8'), end='')
        #cl.send(data)
    # cl.close()
