ws_lcd
==========

TODO

Convenience utility for **WaveShare LCD Displays**.

Supports 128x128 1.44" HAT from Waveshare.
There is an emulation mode (default) which uses Tk to show PIL Image objects.
The advantage of using Tk over using Image.show() is that it will reuse the
same window, so you can show multiple images without opening a new
window for each image (good to simulate display updates). 
The emulation mode is to be used to quickly develop and test display layouts on desktop/laptop.
There is no need to download to RaspberryPi and use real 1.44inch LCD HAT to check the display layout.

Try in the ws_lcd folder: ::

    $ cd ws_lcd/ws_lcd
    $ python layout_1.py

To run in emulation mode, TODO

Install ``ws_lcd`` from source
------------------------------

To use this utility in other projects, install it by: ::

	$ cd ws_lcd
	$ sudo python setup.py develop

Option *develop* installs ``ws_lcd`` in *editable* mode. 
This is very convenient because your changes are immediately reflected into the installed package.
This means that you do not need to re-install ``ws_lcd`` in order your changes to take effect.

Un-install
----------

Un-installing ``ws_lcd`` is easy: ::

	$ cd ws_lcd
	$ sudo python setup.py develop --uninstall


Dependences on Python packages
------------------------------

``ws_lcd`` uses **Tk, Pillow** for emulation and **Pillow, spidev** when using a real display on a RaspberryPi.
Currently, **Pillow** will be installed during the installation of ``ws_lcd`` if not present on your system. 

**Note:** Packages will **not** be un-installed if you un-install ``ws_lcd``. 
