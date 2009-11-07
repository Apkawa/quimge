from setuptools import setup, find_packages
from quimge import quimge

import os
prefix = os.path.join( os.sys.prefix, "share" )
name= "guimge"
data_files = []
for dp, dn, fs in os.walk( os.path.join( name, "icons")):
    temp=[]
    for f in fs:
        temp.append( os.path.join( dp,f ) )
    data_files.append( ( os.path.join( prefix, dp), temp, ) )

data_files.append(
        ( os.path.join( prefix, "pixmaps" ), [os.path.join( name,'icons', 'guimge.png')] ),
)

data_files.append(
        ( os.path.join( prefix, name, "ui" ),
          [os.path.join( name, "ui", "guimge.ui")],
        ))
data_files.append(
        ( "/usr/share/applications/",
          [os.path.join( name, "quimge.desktop") ] ) )

setup(name='guimge',
      version = guimge.VERSION,
      description='quimge - gui for uimge',
      author='Apkawa',
      author_email='apkawa@gmail.com',
      url='http://code.google.com/p/quimge/',
      download_url = 'http://github.com/Apkawa/quimge/',
      license='GPLv3',
      packages=find_packages(),
      data_files=data_files,
      entry_points = {
        'console_scripts':[
            'guimge = guimge:main'
        ]
        }
     )
