#!/usr/bin/python

import os, sys, re, json, shutil
from subprocess import Popen, PIPE, STDOUT

exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten


# Config

emscripten.Settings.USE_TYPED_ARRAYS = 2
emscripten.Settings.CORRECT_OVERFLOWS = 0
emscripten.Settings.CORRECT_ROUNDINGS = 0
emscripten.Settings.CORRECT_SIGNS = 1
emscripten.Settings.OPTIMIZE = 1
emscripten.Settings.RELOOP = 1
emscripten.Settings.INIT_STACK = 0
emscripten.Settings.INVOKE_RUN = 0

emscripten.Building.COMPILER_TEST_OPTS = ['-g']

# Build

print 'Build openjpeg'

output = Popen([emscripten.EMMAKEN, 'common/getopt.c', '-o', 'build/getopt.bc'], stdout=PIPE, stderr=STDOUT).communicate()[0]
assert os.path.exists('build/getopt.bc'), 'Failed to build getopt: ' + output

lib = emscripten.Building.build_library('openjpeg', os.path.join(os.getcwd(), 'build'), os.getcwd(),
                       [
                        os.path.join('bin', 'libopenjpeg.so.1.4.0.bc'),
                        os.path.sep.join('bin/j2k_to_image.bc'.split('/')),
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

f = open('openjpeg.raw.js', 'w')
f.write('''
function openjpeg(data, suffix) {
  var Module = {};
  Module.arguments = [];
  var print = function(){};
''')
f.write(open(filename + '.o.js', 'r').read())
f.write('''
  assert(suffix == 'jp2' || suffix == 'j2k', 'You must specify the suffix as a second parameter. Is this a .j2k or a .jp2 file?');
  FS.init();
  FS.root.write = true;
  FS.createDataFile('/', 'image.' + suffix, data, true, false);

  run(['-i', 'image.' + suffix, '-o', 'image.raw'])
  var ret = {
    width: getValue(_output_width, 'i32'),
    height: getValue(_output_height, 'i32'),
    data: FS.root.contents['image.raw'].contents
  };

  return ret;
}
''')
f.close()

print 'Eliminating unneeded variables'

eliminatoed = Popen([emscripten.COFFEESCRIPT, emscripten.VARIABLE_ELIMINATOR], stdin=PIPE, stdout=PIPE).communicate(open('openjpeg.raw.js', 'r').read())[0]
f = open('openjpeg.elim.js', 'w')
f.write(eliminatoed)
f.close()

print 'Closure compiler'

f = open('openjpeg.elim.js', 'a')
f.write('this["openjpeg"] = openjpeg;')
f.close()

Popen(['java', '-jar', emscripten.CLOSURE_COMPILER,
               '--compilation_level', 'ADVANCED_OPTIMIZATIONS',
               '--js', 'openjpeg.elim.js', '--js_output_file', 'openjpeg.js'], stdout=PIPE, stderr=STDOUT).communicate()

