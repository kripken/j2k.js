
self.onmessage = function(event) {  
  var bytes = event.data.bytes, extension = event.data.extension;
  
  importScripts('../openjpeg.js');
  var j2k = openjpeg(bytes, extension);
  
  self.postMessage(j2k);
};
