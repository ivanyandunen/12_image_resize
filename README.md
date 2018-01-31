# Image Resizer

This script resizes an image and saves it in the same directory or in other existed, specified by user.


# How to use
Python 3 has to be installed. 
You might have to run python3 instead of python depending on system.


```commandline
usage: image_resize.py [-h] -i INPUTFILE [-w WIDTH] [-ht HEIGHT] [-o OUTPATH]
                       [-s SCALE]

optional arguments:
  -h, --help            show this help message and exit
  -i, --inputfile       Path to image file. Required parameter
  -w, --width           New width value.
  -ht, --height         New height value.
  -o, --outpath         Path to resized file. The same as input path by default,
                        if not entered.
  -s, --scale           Value to scale input image. Can be < 1
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
