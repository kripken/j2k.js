import os, sys, re, json, shutil
from subprocess import Popen, PIPE, STDOUT

exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten

data = str(map(ord, open('syntensity_lobby_s.j2k', 'r').read()))
print emscripten.run_js(SPIDERMONKEY_ENGINE, 'runner.js', [data])

