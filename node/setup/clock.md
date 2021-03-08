Guidelines of setting up the system and a sound triggered clock

1. Install raspbian OS on SSD card.
    + (1) Download raspbian lite (version without desktop) from [raspbian website](https://www.raspberrypi.org/software/operating-systems/) 
    + (2) Download and install Etcher from [https://etcher.io/](https://etcher.io/)
    + (3) Open Etcher and format SSD card with Etcher
    + (4) Enable `ssh` by creating an empty file in `/boot` folder:
        ```
        touch ssh
        ```
    + (5) Enable wifi by creating file `wpa_supplicant.conf` in `/boot` folder like this:
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
    + (6) Start raspberry pi, wait for at least 2 minutes and ssh into it:
        ```
        ssh pi@raspberrypi.local  # default pswd is: raspberry
	
        ```
        If there are multiple raspberry pi, try scanning the local network first, for example:
        ```
        nmap -sn 192.168.1.1/24
        ```

2. Basic set up.
    + (1) Install `vim`: `sudo apt-get install vim`
    + (2) Setting in `vim`: `cp ./example_vimrc ~/.vimrc` 
    + (3) Change hostname and password: 
        ```
        passwd
        sudo vim /etc/hostname
        ```

3. Set a fixed (static) IP address for raspberry pi.
	+ (1) `sudo vim /etc/network/interfaces`
    + (2) copy example setting: `cp ./example_interfaces /etc/network/interfaces`
    + (3) `vim /etc/network/interfaces` # change inet IP address
    + (4) `sudo reboot`

4. Set up clock
    + enable PSI: ```sudo raspi-config # -> Interfacing Options -> PSI -> enable PSI;  sudo reboot ```
    + install gpiozero and numpy: `sudo apt-get install python3-gpiozero; sudo apt-get install python3-numpy`
    + run clock script in cron: `sudo crontab -e`, add `@reboot python3 /home/pi/clock.py`

