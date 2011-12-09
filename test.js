
print('loading..');

load(arguments[1]);

print('decoding..');

var data = eval(arguments[0]);
var suffix = arguments[2];
var output1 = openjpeg(data, suffix);
var output2 = openjpeg(data, suffix); // Do it twice for testing purposes

if (JSON.stringify(output1) != JSON.stringify(output2)) throw 'failed to generate 2 identical outputs';

print('result:' + [output2.width, output2.height, output2.data]);

