import os, sys, re, json, shutil
from subprocess import Popen, PIPE, STDOUT

exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten

data = str(map(ord, open('syntensity_lobby_s.j2k', 'r').read()))
output = emscripten.run_js(SPIDERMONKEY_ENGINE, 'test.js', [data])
m = re.search("result:(.*)", output)
array = eval('[' + m.groups(1)[0] + ']')
generated = ''.join([chr(item) for item in array])

out = open('generated.raw', 'wb')
out.write(generated)
out.close()

# check vs reference

reference = open('reference.raw', 'rb').read()
assert reference == generated, 'Failed to generate proper output :('
print 'Success :)'

