import os, sys, re, json, shutil
from subprocess import Popen, PIPE, STDOUT

exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten

for name, suffix, x, y, ref in [['syntensity_lobby_s', 'j2k', 40, 30, 'reference.raw'],
                                ['relax', 'jp2', 400, 300, 'relax.raw']]:
  print 'testing: ' + name + '.' + suffix
  data = str(map(ord, open(name + '.' + suffix, 'r').read()))
  output = emscripten.run_js(SPIDERMONKEY_ENGINE, 'test.js', [data, sys.argv[1], suffix])
  #print output
  m = re.search("result:(.*)", output)
  assert m, 'Failed to generate proper output: %s' % output
  output = eval('[' + m.groups(1)[0] + ']')
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

