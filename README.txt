This is a Circuit Python project based on the Adafruit example described here:
https://learn.adafruit.com/led-acrylic-sign/overview

I do not intend to keep the flash images and Adafruit Neopixel python library on this repo updated -- they are sane at the time of this upload, but you may want to get fresh files from Adafruit.

HARDWARE

I am specifically using the Adafruit Feather M0 Express as the controller for this, with 3 bytes per pixel (not using an RGBW neopixel strip).  This library will NOT work with 4 bytes per pixel (RGBW) neopixels without some major modification.  The only physical modification I've made to the project is to add a button between pin 10 and ground, which is used to change sequences and set the bootloader into edit mode.

INSTALL

Per the directions from Adafruit, pushing the Reset button on the Feather twice lets you flash an image on the Feather.  Flash the Circuit Python image, then copy everything from the Code folder to the root of the controller.  It should take a moment to compile and then reset.  If everything works, it should enter a set of three "High, low, high, off" cycles in different colors.

If you have a button connected, set the pin number in _boot.py and lib/neosequence.py.  If you rename _boot.py to boot.py, it will run when you power up the controller.  If the button is grounded when it runs, it will boot in normal USB-edit mode; otherwise, it boots into a mode where the controller can write to the filesystem but you can no longer edit files over USB.

If the button is held during the start of a transition, it will transition to the start of the next sequence instead of the next step in this sequence.  If boot.py is enabled, your current selection will be remembered if you switch the controller off and on again.

CUSTOMIZING

This library is set up so that main.py only needs to call one function with a list of values.  Therefore, the entirety of that file can be rgb files, helper functions, and comments.  You will want to be comfortable with Python arrays and lambda functions, or else comfortable with reading a long file of explicit arrays.

I tried to document neosequence.py as well as I could.  By all means learn what you can from it and grow.