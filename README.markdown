
j2k.js
======

This is a port of OpenJPEG, an open-source JPEG2000 codec, to JavaScript using Emscripten.

Why? JPEG2000 is useful sometimes, and web browsers don't have native support for it, so having
a pure JS decoder is a nice option to have.


Usage
-----

Grab openjpeg.js which is an optimized and minified build. Then you simply call

  openjpeg([..])

with the argument being an array of values in 0-255 (representing a j2k file in binary format).
The function returns a a JSON object of form

  {
    width: the width
    height: the height
    data: the pixel data (in 24-bit RGB format)
  }


Building
--------

(You don't normally need to do this.)

Do

  python make.py

Looks like you need |make clean| in build/ as incremental builds do not always link.

