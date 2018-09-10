from gpiozero import Button
button = Button(3)

print('waiting for press ...')
button.wait_for_press()
print('pressed!')
