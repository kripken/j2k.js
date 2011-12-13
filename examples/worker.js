
self.onmessage = function(event) {  
  var bytes = event.data.bytes, extension = event.data.extension;
  var t0, t1;
  
  importScripts('../openjpeg.js');
  t0 = (new Date()).getTime();
  var j2k = openjpeg(bytes, extension);
  t1 = (new Date()).getTime();
  
  j2k.tdiff = t1-t0;

  self.postMessage(j2k);
};
