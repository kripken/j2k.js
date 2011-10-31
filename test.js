
print('loading..');

load(arguments[1]);

print('decoding..');

var output = openjpeg(eval(arguments[0]));

print('result:' + [output.width, output.height, output.data]);

