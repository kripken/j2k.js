
j2k.js
======

This is a port of OpenJPEG, an open-source JPEG2000 codec, to JavaScript using Emscripten.

The API is in progress. Right now you can grab openjpeg.js which is an optimized and
minified build. Then you simply call

  openjpeg([..])

with the argument being an array of values in 0-255 (representing a j2k file in binary format).
The function returns a similar array that contains a RAW image, and can be parsed into a canvas
like the emscripten openjpeg demo does etc.

