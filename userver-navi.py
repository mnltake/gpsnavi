#! /home/pi/lv_micropython/ports/unix/micropython

import socket
from struct import unpack
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
buf1_1 = bytearray(1024*5)
draw_buf.init(buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = draw_buf
disp_drv.flush_cb = SDL.monitor_flush
disp_drv.hor_res = 1024
disp_drv.ver_res = 720
disp_drv.register()
# Regsiter SDL mouse driver

indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = SDL.mouse_read
indev_drv.register()

#font
myfont_jp = lv.font_load("S:./font/font-jp-48.bin")
myfont_jp_60 = lv.font_load("S:./font/font-jp-60.bin")
#myfont_jp = lv.font_load("S:%s/font-PHT-jp-48.bin" % script_path)

touch_key="0"

def event_handler(evt):
    code = evt.get_code()
    obj  = evt.get_target()
    if code == lv.EVENT.VALUE_CHANGED :
        id = obj.get_selected_btn()
        touch_key = obj.get_btn_text(id)
        label1.set_text("%s touch"%touch_key)
        print("%s was pressed"%touch_key)
btnm_map = ["A", "B", "C", "S", "W", "D", "V", "R", "E", "M", "H", "P",""]
btnm1 = lv.btnmatrix(lv.scr_act())
btnm1.set_size(1024, 75)
btnm1.set_map(btnm_map)
btnm1.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)
btnm1.add_event_cb(event_handler, lv.EVENT.ALL, None)

#shutdown Button
class Button():
    def __init__(self):
        btn = lv.btn(lv.scr_act())
        btn_red = lv.style_t()
        btn_red.init()
        btn_red.set_bg_color(lv.palette_main(lv.PALETTE.RED))
        style_btn_pressed = lv.style_t()
        style_btn_pressed.init()
        style_btn_pressed.set_bg_color(lv.palette_main(lv.PALETTE.BLUE))
        style_btn_pressed.set_bg_grad_color(lv.palette_darken(lv.PALETTE.BLUE, 3))
        btn.set_size(50, 50)
        btn.set_pos(0, 0)  
        btn.add_style(btn_red, 0)
        btn.add_style(style_btn_pressed, lv.STATE.PRESSED)
        btn.add_event_cb(self.event_cb, lv.EVENT.ALL, None)
        label = lv.label(btn)
        label.set_text("X")
        label.center()



    def event_cb(self,evt):
        code = evt.get_code()
        btnx = evt.get_target()
        if code == lv.EVENT.CLICKED:
            uos.system('sudo shutdown -h now')
        # Get the first child of the button which is the label and change its text
        label = btnx.get_child(0)
        label.set_text("x")

#
# A simple meter
#
meter = lv.meter(lv.scr_act())
meter.align(lv.ALIGN.TOP_MID, 0, 0)
meter.set_size(600,600)

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
style.set_width(250)
style.set_height(lv.SIZE.CONTENT)

#200 
style1 = lv.style_t()
style1.init()
style1.set_bg_color(lv.palette_lighten(lv.PALETTE.GREY, 3))
style1.set_bg_opa(lv.OPA.COVER)
style1.set_bg_grad_color(lv.palette_main(lv.PALETTE.GREY))
style1.set_bg_grad_dir(lv.GRAD_DIR.VER)

# Add a border
style1.set_border_color(lv.color_white())
style1.set_border_opa(lv.OPA._70)
style1.set_border_width(2)
style1.set_radius(50)
style1.set_width(200)
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
#510
style3 = lv.style_t()
style3.init()
style3.set_radius(5)
style3.set_width(510)
style3.set_height(lv.SIZE.CONTENT)
#250
style4 = lv.style_t()
style4.init()
style4.set_radius(5)
style4.set_width(250)
style4.set_height(lv.SIZE.CONTENT)

# nav
txt1 = lv.obj(lv.scr_act())
txt1.remove_style_all() 
txt1.add_style(style1, 0)
txt1.set_pos(420,200)
label1 = lv.label(txt1)
label1.center()
label1.set_style_text_font(myfont_jp, 0)  # set the font
label1.set_text("Wait.. ")
#工程
txt2 = lv.obj(lv.scr_act())
txt2.add_style(style4, 0)
txt2.set_pos(780, 60)  
label2 = lv.label(txt2)
label2.set_style_text_font(myfont_jp, 0)  # set the font
#幅
txt3 = lv.obj(lv.scr_act())
txt3.add_style(style, 0)
txt3.set_pos(0, 60)  
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
txt5.set_pos(0, 400)  
label5 = lv.label(txt5)
label5.set_style_text_font(myfont_jp, 0)  # set the font
#圃場面積
txt6 = lv.obj(lv.scr_act())
txt6.add_style(style3, 0)
txt6.set_pos(0, 500)  
label6 = lv.label(txt6)
label6.set_style_text_font(myfont_jp, 0)  # set the font
#作業面積
txt7 = lv.obj(lv.scr_act())
txt7.add_style(style3, 0)
txt7.set_pos(520, 500)  
label7 = lv.label(txt7)
label7.set_style_text_font(myfont_jp, 0)  # set the font
#基準線
txt8 = lv.obj(lv.scr_act())
# txt8.remove_style_all() 
txt8.add_style(style2, 0)
txt8.set_pos(450, 350)  
label8 = lv.label(txt8)
label8.set_style_text_font(myfont_jp_60, 0)  # set the font
# #速度
# txt9 = lv.obj(lv.scr_act())
# txt9.add_style(style3, 0)
# txt9.set_pos(900, 10)  
# label9 = lv.label(txt9)
# label9.set_style_text_font(myfont_jp, 0)  # set the font


shutdownbtn = Button()
keyname=["0","A","B","C","S","W","D","V","R","Ex","H","M2","SHP"]
blf = False
view =False
oldmsg=[0,0,0,0,0,0,-1,-1,-1,0]
delta=[0,0,0,0,0,0,0,0,0,0]
addr = socket.getaddrinfo('0.0.0.0', 50001)[0][-1]
# print(addr)
s = socket.socket()
s.bind(addr)
s.listen(1)

# print('listening on', addr)
cl, addr = s.accept()
print('client connected ')


while True:
    buff = cl.recv(22)
    # print(cl)
    # print(len(buff))
    if buff:
        newmsg=unpack('hhHHhhIIbb',buff)
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
            if delta[5]:
                label5.set_text("c:%d㎝" %newmsg[5])
            if delta[6]:
                label6.set_text("圃場面積 :%4d㎡" %newmsg[6])
            if delta[7]:
                label7.set_text("作業面積 :%4d㎡" %newmsg[7])
            
            if newmsg[4] < 0 :
                label8.set_text("→" ) 
            else:
                label8.set_text("←" ) 
            #label9.set_text("速度 :%.2fm/s" %navidata[10])
        else:
            key=newmsg[9]
            # print(key)
            label1.set_text("%s pressed"%keyname[key])
            time.sleep(1)
            if key == 7:
                view = not(view)
                if view:
                    uos.system('wmctrl -a "sudo"' )
                else :
                    uos.system('wmctrl -a "TFT Simulator"' )
        oldmsg = newmsg

  
        # print(str(data, 'utf8'), end='')
        #cl.send(data)
    # cl.close()
