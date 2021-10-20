#!/usr/bin/python3
'''
横３＊縦４
薄膜キーパット(3x4) [KEYPAD-UM3X4]
http://www.aitendo.com/product/3644
'''


def keypad_get(*allkey):
    import RPi.GPIO as GPIO
    key_x =allkey[:3]
    key_y =allkey[3:]
    GPIO.setup(key_y,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key_x,GPIO.OUT)
    GPIO.output(key_x[0], GPIO.LOW )
    GPIO.output(key_x[1], GPIO.HIGH )
    GPIO.output(key_x[2], GPIO.HIGH )
    if ( GPIO.input(key_y[0]) == 0 ):
        return 1
    elif ( GPIO.input(key_y[1]) == 0 ):
        return 4
    elif ( GPIO.input(key_y[2]) == 0 ):
        return 7
    elif ( GPIO.input(key_y[3]) == 0 ):
        return 11  # [*]

    GPIO.output(key_x[0], GPIO.HIGH )
    GPIO.output(key_x[1], GPIO.LOW )
    GPIO.output(key_x[2], GPIO.HIGH )
    if ( GPIO.input(key_y[0]) == 0 ):
        return 2
    elif ( GPIO.input(key_y[1]) == 0 ):
        return 5
    elif ( GPIO.input(key_y[2]) == 0 ):
        return 8
    elif ( GPIO.input(key_y[3]) == 0 ):
        return 10 #[0]

    GPIO.output(key_x[0], GPIO.HIGH )
    GPIO.output(key_x[1], GPIO.HIGH )
    GPIO.output(key_x[2], GPIO.LOW )
    if ( GPIO.input(key_y[0]) == 0 ):
        return 3
    elif ( GPIO.input(key_y[1]) == 0 ):
        return 6
    elif ( GPIO.input(key_y[2]) == 0 ):
        return 9
    elif ( GPIO.input(key_y[3]) == 0 ):
        return 12 # [#]

    return  0

if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BOARD)
    key_y = (37 ,35 ,33 ,31 )
    key_x = (29 ,23 ,21)
    while 1:
        key =keypad_get(*key_x, *key_y)
        print(key)
        
