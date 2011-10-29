#!/usr/bin/python

import os, sys, re, json, shutil
from subprocess import Popen, PIPE, STDOUT

exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten


# Config

emscripten.Settings.USE_TYPED_ARRAYS = 0
emscripten.Settings.CORRECT_OVERFLOWS = 1
emscripten.Settings.CORRECT_ROUNDINGS = 1
emscripten.Settings.OPTIMIZE = 1
emscripten.Settings.RELOOP = 0
emscripten.Settings.INIT_STACK = 1
emscripten.Settings.INVOKE_RUN = 0

if emscripten.Settings.USE_TYPED_ARRAYS == 2:
  emscripten.Settings.CORRECT_SIGNS = 1
else:
  emscripten.Settings.CORRECT_SIGNS = 1
  emscripten.Settings.CORRECT_SIGNS_LINES = ["mqc.c:566", "mqc.c:317"]
  emscripten.Building.COMPILER_TEST_OPTS = ['-g']


# Build

print 'Build openjpeg'

output = Popen([emscripten.EMMAKEN, 'common/getopt.c', '-o', 'build/getopt.bc'], stdout=PIPE, stderr=STDOUT).communicate()[0]
assert os.path.exists('build/getopt.bc'), 'Failed to build getopt: ' + output

lib = emscripten.Building.build_library('openjpeg', os.path.join(os.getcwd(), 'build'), os.getcwd(),
                       [
                        os.path.join('bin', 'libopenjpeg.so.1.4.0.bc'),
                        os.path.sep.join('bin/j2k_to_image.bc'.split('/')),
                        'getopt.bc',
                        #os.path.sep.join('codec/CMakeFiles/j2k_to_image.dir/index.c.o'.split('/')),
                        #os.path.sep.join('codec/CMakeFiles/j2k_to_image.dir/convert.c.o'.split('/')),
                        #os.path.sep.join('codec/CMakeFiles/j2k_to_image.dir/__/common/color.c.o'.split('/')),
                       ],
                       configure=['cmake', '..'],
                       #configure_args=['--disable-png', '--disable-tiff', '--disable-lcms2', '--disable-lcms1'],
                       make_args=[]) # no -j 2, since parallel builds can fail

print 'LLVM dis'

filename = 'build/bc.bc'
shutil.move(filename, filename + '.o') # Use the filename conventions in the emscripten build system
emscripten.Building.llvm_dis(filename)

if 0:
  print '[Autodebugger]' # XXX Probably should run this script with EMMAKEN_NO_SDK=1, for the bc to be runnable in lli
                         #     Then do        ~/Dev/emscripten/tools/exec_llvm.py bc.bc.o -i image.j2k -o image.raw

  shutil.move('build/bc.bc.o.ll', 'build/bc.bc.orig.o.ll')
  output = Popen(['python', emscripten.AUTODEBUGGER, 'build/bc.bc.orig.o.ll', 'build/bc.bc.o.ll'], stdout=PIPE, stderr=STDOUT).communicate()[0]
  assert 'Success.' in output, output

  shutil.move('build/bc.bc.o', 'build/bc.bc.orig.o')
  print Popen([emscripten.LLVM_AS, 'build/bc.bc.o.ll', '-o=build/bc.bc.o']).communicate()

print 'Emscripten'

emscripten.Building.emscripten(filename)

print 'Bundle'

f = open('openjpeg.js', 'w')
f.write('''
var openjpeg = (function() {
  var Module = {};
  Module.arguments = [];
''')
f.write(open(filename + '.o.js', 'r').read())
f.write('''
  return function(data) {
    FS.init();
    FS.root.write = true;
    FS.createDataFile('/', 'image.j2k', data, true, false);
    run(['-i', 'image.j2k', '-o', 'image.raw'])
    return FS.root.contents['image.raw'].contents;
  };
})();
''')
f.close()

