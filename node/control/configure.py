from gpiozero import MCP3008 

pin_airtq = 17

pin_sound = 26
channel_sound = 0

pin_light = 17
channel_light = 1

pin_soilq = 27
channel_soilq = 2

pin_soilt = 4

path_picout = '/home/pi/farm/data/pictures/'

path_ssout = '/home/pi/farm/data/sensors/'

node = 'n001002'

filetimegap   = 60  # time gap between files: 60 seconds

dt_restart = 3600 # restart camera and sensors: 1 hour

daytime = [6, 18]

motion_conf_day = 'motion.conf_day'

motion_conf_night = 'motion.conf_night'

keepdays = {'airtq':7, 'sound':7, 'light':7, 'soilq':7, 'soilt':7, 
        'snapshot':7, 'motion':7}

