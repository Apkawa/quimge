from setuptools import setup, find_packages
from PyQt4.uic import compileUiDir

def needsupdate(src, targ):
    return not os.path.exists(targ) or os.path.getmtime(src) > os.path.getmtime(targ)

def compile_qrc(qrc_file, py_file):
        if not needsupdate(qrc_file, py_file):
            return
        print("compiling %s -> %s" % (qrc_file, py_file))
        try:
            import subprocess
            rccprocess = subprocess.Popen(['pyrcc4', qrc_file, '-o', py_file])
            rccprocess.wait()
        except Exception, e:
            raise distutils.errors.DistutilsExecError, 'Unable to compile resouce file %s' % str(e)
            return

import os
prefix = os.path.join( os.sys.prefix, "share" )
name= "quimge"
data_files = []
for dp, dn, fs in os.walk( os.path.join( name, "icons")):
    temp=[]
    for f in fs:
        if f.startswith('.png'):
            temp.append( os.path.join( dp,f ) )
    data_files.append( ( os.path.join( prefix, dp), temp, ) )

data_files.append(
        ( os.path.join( prefix, "pixmaps" ), [os.path.join( name,'icons', 'quimge.png')] ),
)

data_files.append(
        ( "/usr/share/applications/",
          [os.path.join( name, "quimge.desktop") ] ) )
print data_files

compileUiDir( os.path.join(name,'ui') )
compile_qrc( os.path.join( name, 'icons','gtk_stock.qrc' ),os.path.join( name, 'icons','gtk_stock_rc.py' ) )


import quimge

setup(name='quimge',
      version = quimge.VERSION,
      description='quimge - gui for uimge',
      author='Apkawa',
      author_email='apkawa@gmail.com',
      url='http://code.google.com/p/quimge/',
      download_url = 'http://github.com/Apkawa/quimge/',
      license='GPLv3',
      packages=find_packages(exclude=('uimge')),
      data_files=data_files,
      entry_points = {
        'console_scripts':[
            'quimge = quimge:main'
        ]
        }
     )
