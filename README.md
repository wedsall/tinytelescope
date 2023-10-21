# tinytelescope
DIY raspberry pi / le potato photo box for Space Geeks

I made this using a Libre Computer (Le Potato) https://libre.computer/products/aml-s905x-cc/. You could use a Raspberry Pi as well but I recommend at least 1GB of memory (2+ better) because some of the space images can be huge.

## Who needs this?

Make this for yourself, a friend or family member who loves everything space. Connect it up to a tv or monitor, power it up and let it go. This loops through Hubble and James Webb telescope high resolution images and also displays the text that is included on each photo's page. The title of the image is displayed on the top right. Images cycle every 30-60 seconds and can be configured to your liking.

This current version does not disable at night because the Le Potato I was using didn't seem to have that functionality. If you know how to do it, please help. :)

It is expected that you have some basic linux knowledge and python knowledge.

## How it works

Your system will need python3 and all of the packages needed by download.py and photos.py.

You will need to download the images. This download.py script reads the data from all_image_info5.json and will attempt to download every file. 
<code>python3 download.py</code>

Next create a startup script on your device. For the Le Potato this was ~/.config/autostart/digital_frame.desktop
<code>
:~/.config/autostart $ more digital_frame.desktop
[Desktop Entry]
Type=Application
Name=Digital Photo Frame
Exec=/home/whoever/photos.sh
</code>

Next create the photos.sh script:
<code>
#!/bin/bash

/usr/bin/python3 /home/whoever/photos.py @> /dev/null
</code>

Reboot and it should start.

## Files

| File | Description |
| --- | ----------- |
| all_image_info5.json | A curated list of Hubble and James Webb top photos |
| download.py | Used for downloading the photos to your device |
| get_image_data.py | The code I used to pull the photo data. You can modify and use this as needed |
| photos.py | The code that runs the device. |
| digital_frame.desktop | On Le Potato this goes in ~/.config/autostart/ to automatically start the photos.py program on startup |
| photos.sh | A shell script to start the program |
