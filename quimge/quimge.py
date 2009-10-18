#!/usr/bin/python
# -*- coding: utf-8 -*-
###
#This file is part of <name prog> project
#
#<описание программы>
#Copyright (C) <year> <name|nick>
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#You can contact author by email <my email>
###
from PyQt4 import QtCore, QtGui, uic
DEBUG = True
if DEBUG:
    Ui_qUimge_main = uic.loadUiType("ui/main.ui")[0]
    Ui_About = uic.loadUiType("ui/about.ui")[0]
else:
    from ui.main import Ui_qUimge_main

from icons import gtk_stock_rc
import sys, os

import uimge
def About(parent=None):
        about_dialog = Ui_About()
        dialog = QtGui.QDialog( parent )
        about_dialog.setupUi( dialog )
        return dialog


class qUimge( QtGui.QMainWindow ):
    default_host = 'radikal.ru'
    Uimge = uimge.Uimge()
    Outprint = uimge.Outprint()
    result = []
    delimiter = r'\n'
    image_type = ('.png', '.jpe', '.jpg', '.jpeg', '.gif', '.bmp')
    def __init__(self, parent=None):
        '''docstring for __init__'''
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QWidget.__init__(self, parent)
        #self.app.setStyle("windows")
        self.WidgetsTree = Ui_qUimge_main()
        self.WidgetsTree.setupUi( self )
        self.clipboard = self.app.clipboard()
        self.progressBar = self.WidgetsTree.progressBar
        self.progressBar.setMinimum( 0)
        self.BoxProgress = self.WidgetsTree.BoxProgress
        self.BoxProgress.hide()

        self.upload_list = self.WidgetsTree.UploadList
        self.WidgetsTree.UploadTab.installEventFilter( self) #set key press for upload tab

        self.about_dialog = About(self)


        style = self.app.style()
        self._init_SIGNALS()
        self._initSelectHost()

        self.WidgetsTree.ModePrint.addItem( "Direct url", QtCore.QVariant("Direct") )
        for k, v in self.Outprint.outprint_rules.items():
            self.WidgetsTree.ModePrint.addItem( v['desc'], QtCore.QVariant( k) )
        self.WidgetsTree.Delimiter.addItem(r"\n")

    def run(self, files=None):
        '''docstring for run'''
        self.show()
        self._initFileListIcons(files)
        sys.exit( self.app.exec_() )
    def exit(self):
        self.close()
        sys.exit()
    def eventFilter(self, obj, event):
        #http://www.commandprompt.com/community/pyqt/x5469
        #http://www.nabble.com/Mayavi,-VTK-and-PyQt-td21894370.html
        #        print obj, event
        if type(event) == QtGui.QKeyEvent:
            if QtGui.QKeySequence.Delete == event:
                self._clear_selected()
        return QtGui.QWidget.eventFilter(self, obj, event)
    def keyPress_Event(self, event):
        print event
        event.ignore()


    def _init_SIGNALS(self):
        '''docstring for _init_SIGNALS'''
        connect = self.connect
        SIGNAL = QtCore.SIGNAL
        SLOT = QtCore.SLOT
        connect(self.WidgetsTree.action_Open, SIGNAL("activated()"), self._open_file)
        connect(self.WidgetsTree.actionLoad_images, SIGNAL("activated()"), self._open_file)
        connect(self.WidgetsTree.actionLoad_images_from_folder, SIGNAL("activated()"), self._open_folder)
        connect(self.WidgetsTree.actionAbout, SIGNAL("activated()"), self.about_dialog.exec_ )
        connect(self.WidgetsTree.actionUpload, SIGNAL("activated()"), self._upload)
        connect(self.WidgetsTree.actionUpload_2, SIGNAL("activated()"), self._upload)
        connect(self.WidgetsTree.actionClipboard, SIGNAL("activated()"), self._copy_to_clipboard)

        connect(self.WidgetsTree.ModePrint, SIGNAL("textChanged(QString)"), self._update_result)
        connect(self.WidgetsTree.ModePrint, SIGNAL("currentIndexChanged(int)"), self._update_result)
        connect(self.WidgetsTree.Delimiter, SIGNAL("textChanged(QString)"), self._set_delim)
        connect(self.WidgetsTree.DeleteSelected, SIGNAL("clicked()"), self._clear_selected)

        connect( self.upload_list, SIGNAL("itemSelectionChanged()"), self._update_summary)
        connect( self.WidgetsTree.ClearUploadList, SIGNAL("clicked()"), self._update_summary)
        connect( self.WidgetsTree.DeleteSelected, SIGNAL("clicked()"), self._update_summary)


    def _initFileListIcons(self, filenames=None):
        '''
        Create File List
        '''
        self._update_summary()
        if filenames:
            self._add_files( filenames )

    def _initSelectHost(self):
        def get_favicon( host, ico_path):
            #TODO переписать на Qt
            if not os.path.exists(ico_path):
                import urllib
                u = urllib.urlopen('http://favicon.yandex.net/favicon/%s'%host).read()
                #http://www.google.com/s2/favicons?domain=www.labnol.org
                tmp = open( '/tmp/tmp.png','w+b')
                tmp.write( u )
                tmp.close()
                tmp_ico = QtGtk.QPixmap("/tmp/tmp.png")
                if tmp_ico.width() == 1:
                    _ico = fail_icon
                    fail_icon.save( ico_path, "png" )
                else:
                    _ico = tmp_ico.scale_simple( 16,16, gtk.gdk.INTERP_HYPER)
                    tmp_ico.save( ico_path,"png" )
            else:
                _ico = QtGui.QPixmap( ico_path )

            return _ico

        "Устанавливаем выпадающий список выбора хостингов c иконостасом"
        fail_icon = QtGui.QIcon( QtGui.QPixmap(':/app/guimge.py') )

        ico_dir = os.path.join( 'icons', 'hosts')
        selhost  = self.WidgetsTree.SelectHost
        _hosts = dict([(v.host,QtCore.QVariant( v ) ) for k,v in uimge.Hosts.hosts_dict.items()])
        _h = sorted(_hosts.keys() )
        for host in _h:
            ico_name = host+'.png'
            ico_path = os.path.join( ico_dir,ico_name)
            ico = QtGui.QIcon( QtGui.QPixmap( ico_path ) )
            selhost.addItem( ico, host, _hosts.get( host) )
        selhost.setCurrentIndex( _h.index( self.default_host ))

    def _add_file(self, _file):
        '''docstring for _add_file'''
        thumb_size = 100
        max_length_filename = thumb_size/9

        _uf = unicode(_file, 'utf-8')
        _qf = QtCore.QString(_file )
        fileinfo = QtCore.QFileInfo( _qf)

        px = QtGui.QPixmap( _qf )
        _qsize = px.size()
        if _qsize.isNull():
            return
        filename = fileinfo.fileName()
        size = fileinfo.size()
        size_str = human( size )

        if len(filename) > max_length_filename:
            filename = '%s...%s'%(
                    filename[0:max_length_filename/2 ],filename[-max_length_filename/2:],
                    )
        else:
            filename = '%s'%(
                    filename,
                    )
        text_item ="%(name)s \n [%(size)s]"%{'size': size_str, 'name':filename }

        icon = QtGui.QIcon()
        icon.addPixmap( px.scaledToHeight( thumb_size )  )
        data = {'path':_qf,'size': size, 'human_size': size_str, 'fileinfo':fileinfo }
        item = QtGui.QListWidgetItem( icon, text_item, self.upload_list )
        item.setData( QtCore.Qt.UserRole,QtCore.QVariant( data ) )
        item.setToolTip( _uf)
        item.setSizeHint( QtCore.QSize( thumb_size+23,thumb_size+46) )

    def _add_files(self, _files):
        '''docstring for _add_files'''
        file_list = []
        for f in _files:
            if not os.path.isdir( f):
                file_list.append(f)
            else:
                for filename in os.listdir( f ):
                    path = os.path.join( str(f), filename)
                    if os.path.isfile( path ):
                        file_list.append( path )

        current_file_count = 0
        files_count = len(file_list)

        self.BoxProgress.show()
        self.progressBar.setMaximum( files_count )
        for f in file_list:
            self.progressBar.setValue( current_file_count )
            self._add_file( f)
            while self.app.processEvents():
                pass
            self._update_summary()
            current_file_count += 1

        self.BoxProgress.hide()
        self.progressBar.setValue(0)

    def _update_summary(self):
        '''docstring for calculate_summary'''
        all_files = self.upload_list.count()
        all_size  = 0
        selected  = 0
        selected_size = 0L
        for i in xrange(all_files):
            item = self.upload_list.item(i)
            data = item.data( QtCore.Qt.UserRole).toPyObject()
            size = data.get( QtCore.QString('size') )
            all_size += size
            if item.isSelected():
                selected += 1
                selected_size += size
        if selected:
            status_str = "Selected %s images (%s)"%( selected, human( selected_size) )
        else:
            status_str = "%s images (%s)"%( all_files, human( all_size) )

        self.WidgetsTree.statusBar.showMessage( status_str )


    def _open_file(self):
        '''docstring for _open_file'''
        dialog = QtGui.QFileDialog( )
        filename = dialog.getOpenFileNames( self,"select images", "/home/apkawa","images (*%s)" % ' *'.join([ i for i in self.image_type]))

        self._add_files( filename)
    def _open_folder(self):
        '''docstring for _open_folder'''
        dialog = QtGui.QFileDialog( )
        filename = dialog.getExistingDirectory( self,"select folder", "/home/apkawa" )
        self._add_files( [filename])


    def _clear_selected(self):
        '''docstring for _clear_selected'''
        items = self.upload_list.selectedItems()
        for i in items:
            it = self.upload_list.takeItem( self.upload_list.row(i))
            it = None
        self._update_summary()

    def _set_current_host( self):
        cur_h  = self.WidgetsTree.SelectHost.currentIndex()
        host_key = self.WidgetsTree.SelectHost.itemData(cur_h).toPyObject()
        self.Uimge.set_host( host_key   )
    def _upload(self):
        '''docstring for _upload'''
        self.result = []
        def _uploading_thread():
            pass
        self._set_current_host()
        count = self.upload_list.count()
        self.progressBar.setMaximum( count )
        self.BoxProgress.show()
        for i in xrange( count ):
            item = self.upload_list.item(i)
            data = item.data( QtCore.Qt.UserRole).toPyObject()
            path = data.get( QtCore.QString('path') )
            self.Uimge.upload( path)
            while self.app.processEvents():
                pass
            print self.Uimge.img_url
            self.result.append( ( self.Uimge.img_url,
                    self.Uimge.img_thumb_url,
                    self.Uimge.filename
                    ) )
            self.progressBar.setValue( i )

        self.BoxProgress.hide()
        self.progressBar.setValue( 0 )
        self._update_result()

    def _update_result(self, index_or_str=None):
        '''docstring for _update_result'''
        if index_or_str:
            mp = self.WidgetsTree.ModePrint
            ci = mp.currentIndex()
            if type( index_or_str) == int:
                if mp.itemData(index_or_str).isValid():
                    self.Outprint.set_rules( key=str(mp.itemData(index_or_str).toString()) )
                else:
                    self.Outprint.set_rules( usr=str(mp.itemText(index_or_str)) )
            elif type( index_or_str ) == QtCore.QString and mp.itemData(ci).isNull():
                    self.Outprint.set_rules( usr=str(index_or_str) )


        _result = self.delimiter.join([ self.Outprint.get_out( r[0], r[1], r[2]) for r in self.result] )
        if _result:
            self.WidgetsTree.ResultText.setPlainText( _result)
            self._copy_to_clipboard()
            return True
        else:
            return False
    def _set_delim(self, delim):
        self.delimiter = str(self.WidgetsTree.Delimiter.currentText()).replace("\\n",'\n')
        self._update_result()
    def _copy_to_clipboard(self):
        '''docstring for copy_to_clipboard'''
        self.clipboard.clear()
        text = self.WidgetsTree.ResultText.toPlainText()
        self.clipboard.setText( text)

    def _test(self):
        def StandardIcon():
            for d in dir(QtGui.QStyle):
                if d.startswith('SP_'):
                    icon = self.app.style().standardIcon( QtGui.QStyle.__dict__[d] )
                    icon.actualSize( QtCore.QSize( 50,50) )
                    item = QtGui.QListWidgetItem( icon, d , self.upload_list)
                    item.setSizeHint( QtCore.QSize( 100+23,100+46) )
        StandardIcon()


def human(num, prefix=" ", suffix='b'):
    num=float(num)
    for x in ['','K','M','G','T']:
        if num<1024:
            return "%3.1f%s%s%s" % (num, prefix, x,  suffix)
        num /=1024

def  main( *args, **kwargs):
    """
    main()
    """
    qu = qUimge()
    #qu._test()
    qu.run(files=sys.argv[1:])



if __name__ == "__main__":
    main()
