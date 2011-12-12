import os, sys, re, json, shutil
from subprocess import Popen, PIPE, STDOUT

exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten

for name, suffix, x, y, ref in [['syntensity_lobby_s', 'j2k', 40, 30, 'reference.raw'],
                                ['relax', 'jp2', 400, 300, 'relax.raw']]:
  print 'testing: ' + name + '.' + suffix
  data = str(map(ord, open(name + '.' + suffix, 'r').read()))
  raw = emscripten.run_js('test.js', SPIDERMONKEY_ENGINE, [sys.argv[1], data, suffix])
  sets = raw.split('*')
  output = eval('[' + sets[1] + ']')
  width = output[0]
  height = output[1]
  data = ''.join([chr(item) for item in output[2:]])

  out = open('generated.raw', 'wb')
  out.write(data)
  out.close()

  # check

  assert width == x, 'Failed to generate proper width: %d' % width
  assert height == y, 'Failed to generate proper height: %d' % height

  reference = open(ref, 'rb').read()
  assert reference == data, 'Failed to generate proper output :('

print 'Success :)'

