# Method 3R for environment protection

## Motivation

Today more and more Vietnamese are aware of environmental issues, amongst them daily waste concerns everyone. Slogan and propaganda are many, but concret actions are too neglected. This project is born to fill that gap between green spirit and green actions.

## How it works

3R is a famous mnemotechnic to remind how to deal with a certain type of product. 3R represents *recycle, reduce, reuse*. In Vietnamese, they are translated into 3T: *tái chế, tiết giảm, tái sử dụng*.

The player will choose one of the 3 Rs, and one of the given products. The machine will suggest a way to protect the environment based on the player's choices.

Play the video below to grasp what all of this is about:
    
[![](http://img.youtube.com/vi/sBtvLVopoT8/0.jpg)](https://youtu.be/sBtvLVopoT8)

## Pre-requisites

Materials:
    
* 2 NFC reader modules as in [our multiple-objects detection system](https://github.com/quantranfr/MultiNFC);
* 3 daisy-chained LED matrix modules (32x64 full color) and a Raspberry Pi (tested with a 4b) as described in [my LED matrix investigation](https://github.com/quantranfr/LEDMatrix).

Libraries and code setup:
    
* Download [MultiNFC](https://github.com/quantranfr/MultiNFC)
* Download [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix/)

  * Go to the subfolder `examples-api-use` and run `make`; this will generate the `demo` executable that we will use in our program;
  * Run `sudo setcap 'cap_sys_nice=eip' demo` to be able to run `demo` correctly (no flickering) without `sudo`.
  * Open `/boot/config.txt` in sudo mode and change the line `dtparam=audio=on` to `dtparam=audio=off`;

* Install `pango` with `sudo apt-get install -y libsdl-pango-dev`. In MacOS: `brew install pango`.

## Run the program

Follow these steps:
    
* Run `python main.py` in this repository.
* Run `python readSerial.py` in MultiNFC.

## Roadmap

* Make a second LED matrix line to display user's choices.