
j2k.js
======

This is a port of OpenJPEG, an open-source JPEG2000 codec, to JavaScript using Emscripten.

The API is in progress. Right now you can grab openjpeg.js which is an optimized and
minified build. Then you simply call

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

Do

  python make.py

Looks like you need |make clean| in build/ as incremental builds do not always link.

