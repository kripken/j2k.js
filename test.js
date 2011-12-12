
print('loading..');

load(arguments[0]);

print('decoding..');

var i = 1;
while (i < arguments.length) {
  var data = eval(arguments[i]);
  var suffix = arguments[i+1];
  var output1 = openjpeg(data, suffix);
  var output2 = openjpeg(data, suffix); // Do it twice for testing purposes
  if (JSON.stringify(output1) != JSON.stringify(output2)) throw 'failed to generate 2 identical outputs';

  print('*' + [output2.width, output2.height, output2.data] + '*');

  i += 2;
}

