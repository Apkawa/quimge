from distutils.core import setup
import py2exe
import glob
import os

from PyQt4.uic import compileUi
def compileUiDir( path):
    for f in os.listdir( path):
        if f.endswith('.ui'):
            compileUi( os.path.join(path,f ),
                    open(os.path.join(path,f[:-3] )+'.py','w') )



#compileUiDir( os.path.join( 'quimge','ui') )

setup(
    name = 'quimge',
    description = 'Multiuploading image',
    version ="0.0.1" ,

    #console = [
    windows = [
                  {
                      'script': 'quimge/quimge.py',
                      'icon_resources': [(1, "quimge/icons/quimge.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings, uimge',
                      'includes':'sip,curl',
                      "skip_archive": True,
                  }
              },

    data_files=[
                    ('icons',glob.glob('quimge/icons/*.*'), ),
                    #('ui',glob.glob('quimge/ui/*.*'), ),
                    ('icons/hosts',glob.glob('quimge/icons/hosts/*.png'),),
                    ('imageformats', glob.glob('C:\Python25\Lib\site-packages\PyQt4\plugins\imageformats\*.*')),
                   #('ui',['quimge/ui/main.ui']),   
                   ]
)
