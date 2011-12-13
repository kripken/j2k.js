
self.onmessage = function(event) {  
  var bytes = event.bytes, extension = event.extension;
  
  importScripts('../openjpeg.js');
  var j2k = openjpeg(bytes, extension);
  
  self.postMessage(j2k);
};
