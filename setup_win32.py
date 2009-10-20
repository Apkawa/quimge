from distutils.core import setup
import py2exe
import glob

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
                    ('ui',glob.glob('quimge/ui/*.*'), ),
                    ('icons/hosts',glob.glob('quimge/icons/hosts/*.png'),),
                    ('imageformats', glob.glob('C:\Python25\Lib\site-packages\PyQt4\plugins\imageformats\*.*')),
                   #('ui',['quimge/ui/main.ui']),   
                   ]
)
