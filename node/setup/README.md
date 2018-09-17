Guidelines of setting up the system

+ 1. Install raspbian OS on SSD card.
    + (1) Download raspbian (version without desktop) from [raspbian website](https://www.raspberrypi.org/downloads/raspbian/) 
    + (2) Download and install Etcher from [https://etcher.io/](https://etcher.io/)
    + (3) Open Etcher and format SSD card with Etcher
    + (4) Enable `ssh` by creating an empty file in `/boot` folder:
```
touch ssh
```
    (5) Enable wifi by creating file `wpa_supplicant.conf` in `/boot` folder like this:
        ```
        country=US
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        network={
            ssid="SSID"
            psk="PASSWORD"
            key_mgmt=WPA-PSK
            }
        ```
    (6) Start raspberry pi and ssh into it:
        ```
        ssh pi@raspberrypi.local
        ```
        If there are multiple raspberry pi, try scanning the local network first:
        ```
        nmap -sn 192.168.1.1/24
        ```

3. Basic set up.
    (1) Install `vim`: `sudo apt-get install vim`
    (2) Setting in `vim`: `cp ./example_vimrc ~/.vimrc` 
    (3) Change hostname and password: 
        ```
        passwd
        sudo vim /etc/hostname
        ```

4. Set a fixed (static) IP address for raspberry pi.
	(1) `sudo vim /etc/network/interfaces`
    (2) copy example setting: `cp ./example_interfaces /etc/network/interfaces`
    (3) `vim /etc/network/interfaces` # change inet IP address
    (4) `sudo reboot`

5. Set up camera
    (1) install driver:
            sudo modprobe bcm2835-v4l2  # then you should get /dev/video0
    (2) install motion:
            sudo apt-get install motion
    (3) set up configure 
            sudo cp /etc/motion/motion.conf ~/.motion/motion.conf
            # set target_dir, width, height, stream_localhost, etc.
            # for detailed setting in config, see https://www.bouvet.no/bouvet-deler/utbrudd/building-a-motion-activated-security-camera-with-the-raspberry-pi-zero
    (4) start motion
            sudo motion -c ~/.motion/motion.conf

6. Set up websever
    (1) sudo apt-get install apache2 -y
    (2) link you file in /var/www/html/


