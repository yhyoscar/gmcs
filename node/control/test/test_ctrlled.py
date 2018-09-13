from gpiozero import LED, Button
from time import sleep
from signal import pause

def switch_led(led, button):
    while True:
        print('waiting for pressing ...')
        button.wait_for_press()
        print('pressed!')
        
        led.toggle()
        sleep(0.5)
        
        #led.on()
        #print('led: on')
        #sleep(3)
        #led.off()
        #print('led: off')
    return

def hold_release(led, button):
    button.when_pressed = led.on
    print('led: on')
    button.when_released = led.off
    print('led: off')
    pause()
    return


if __name__ == '__main__':
    led = LED(2)
    button = Button(3)
    print('------ finished initialization ------')
    hold_release(led, button)    


