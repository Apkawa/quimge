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
import os
import sys
import copy

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QPixmap,QIcon
from PyQt4.QtCore import QString, QDir, QFileInfo, QVariant
DEBUG = False

if not DEBUG:
    if sys.platform != 'win32':
        from ui.main import Ui_qUimge_main
        from ui.about import Ui_qUimge_about
        from ui.setting import Ui_Dialog as Ui_qUimge_setting
    else:
        from quimge.ui.main import Ui_qUimge_main
        from quimge.ui.about import Ui_qUimge_about
        from quimge.ui.setting import Ui_Dialog as Ui_qUimge_setting
else:
    from PyQt4 import uic
    Ui_qUimge_main = uic.loadUiType("ui/main.ui")[0]
    Ui_qUimge_about = uic.loadUiType("ui/about.ui")[0]
    Ui_qUimge_setting = uic.loadUiType("ui/setting.ui")[0]




from icons import gtk_stock_rc

from uimge import uimge
HOSTS = dict(
            [ (v.host, QtCore.QVariant( v ) )
                for k,v in uimge.Hosts.hosts_dict.items()]
            )

APPNAME = 'quimge'
ORGNAME = 'Apkawa Inc'
VERSION = '0.0.3'

def module_path():
    if hasattr(sys, "frozen"):
        return os.path.dirname(
            unicode(sys.executable, sys.getfilesystemencoding( ))
        )
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
SCRIPT_DIR = os.path.abspath(module_path())
print SCRIPT_DIR

def make_hosts_combobox(combobox=None, default_host=None):
    def get_favicon( host, ico_path):
        fail_pixmap = QPixmap(':/app/text-html.png')
        if not os.path.exists(ico_path):
            import urllib
            u = urllib.urlopen('http://favicon.yandex.net/favicon/%s'%host).read()
            #http://www.google.com/s2/favicons?domain=www.labnol.org
            tmp = open( '/tmp/tmp.png','w+b')
            tmp.write( u )
            tmp.close()
            pixmap = QPixmap("/tmp/tmp.png")
            if pixmap.size() == QtCore.QSize(1, 1):
                pixmap = fail_pixmap
            tmp_ico = QIcon( pixmap )
            pixmap.save( QString( ico_path) )

        return tmp_ico

    "Устанавливаем выпадающий список выбора хостингов c иконостасом"

    ico_host_dir = os.path.join(  SCRIPT_DIR ,'icons','hosts')
    if not os.path.exists( ico_host_dir):
        ico_host_dir = os.path.join(
                os.sys.prefix,
                'share',
                'quimge',
                'icons',
                'hosts')

    if isinstance(combobox, QtGui.QComboBox):
        selhost  = combobox
    else:
        selhost  = QtGui.QComboBox()

    for host, obj in HOSTS.items():
        ico_name = host+'.png'
        ico_path = os.path.join( ico_host_dir,ico_name)
        ico = QIcon( QPixmap( ico_path ) )
        if ico.isNull():
            ico = get_favicon( host, ico_path)
        selhost.addItem(ico, " %s"%host, QVariant([host, obj]) )
    if default_host:
        index = selhost.findText( default_host, QtCore.Qt.MatchEndsWith )
        selhost.setCurrentIndex( index if index else 1 )
    return selhost

class Setting:
    def __init__(self, parent=None):
        '''docstring for __init__'''
        if not parent:
            self.setting = QtCore.QSettings(
                    #QtCore.QSettings.IniFormat,
                        QtCore.QSettings.NativeFormat,
                        QtCore.QSettings.UserScope,
                        APPNAME,
                        APPNAME,
                    )
        else:
            self.setting = parent

    def begin_group(self, groupname):
        self.setting.beginGroup( groupname )

    def end_group(self):
        self.setting.endGroup()

    def set(self, key, val):
        '''docstring for set'''
        self.setting.setValue( key, QVariant( val ) )

    def get(self, key, default=''):
        '''docstring for get'''
        _res = self.setting.value( key )
        if _res.isNull():
            default = QString(default)
            self.set(key, default )
            return default
        else:
            return _res.toString()

    def save(self):
        print self.setting.fileName()
        self.setting.sync()

def About(parent=None):
    about_dialog = Ui_qUimge_about()
    dialog = QtGui.QDialog( parent )
    about_dialog.setupUi( dialog )
    return dialog

class qUimge_setting_dialog( object):
    def __init__(self, setting, parent=None):
        '''docstring for __init__'''

        self.setting_dialog = Ui_qUimge_setting()
        self.dialog = QtGui.QDialog( parent )
        self.setting_dialog.setupUi( self.dialog )
        self.Setting = setting
        self.set_signals()

        self.style = self.Setting.get('style')
        self.default_host = self.Setting.get('default_host')
        self.start_dir = self.Setting.get("startdir", QtCore.QDir().homePath())

        self.setting_dialog.list_styles.addItems( QtGui.QStyleFactory.keys() )
        self.setting_dialog.list_styles.setCurrentIndex( self.setting_dialog.list_styles.findText( self.style) )
        self.select_default_host = self.setting_dialog.select_default_host
        make_hosts_combobox( self.select_default_host, self.default_host )

        self.setting_dialog.start_dir_edit.setText(self.start_dir)



    def set_signals(self):
        connect = self.dialog.connect
        SIGNAL = QtCore.SIGNAL
        SLOT = QtCore.SLOT
        connect( self.setting_dialog.buttonBox, SIGNAL("accepted()"), self.accept)
        connect( self.setting_dialog.select_start_dir, SIGNAL("clicked()"), self.open_folder)

    def open_folder(self):
        '''docstring for _open_folder'''
        dialog = QtGui.QFileDialog( )
        filename = dialog.getExistingDirectory(self.dialog,
                "Select folder",
                self.start_dir )
        if filename:
            start_dir = QtCore.QFileInfo( filename ).absoluteFilePath()
            self.setting_dialog.start_dir_edit.setText(start_dir)

    def exec_(self):
        self.dialog.exec_()
    def accept(self):
        cur_h  = self.select_default_host.currentIndex()
        host, obj = self.select_default_host.itemData(cur_h).toPyObject()
        self.Setting.set("default_host", host)
        self.Setting.set("style", self.setting_dialog.list_styles.currentText())
        self.Setting.set("startdir", self.setting_dialog.start_dir_edit.text())
        self.dialog.accept()

class UploadThread( QtCore.QThread):
    def __init__(self, parent=None):
        '''docstring for __init__'''
        QtCore.QThread.__init__( self, parent)
        self.uploading = True
        pass
    def setup(self, Uimge,  path):
        self.uploading = True
        self.Uimge = Uimge
        self.path = path
    def run(self):
        self.Uimge.upload( self.path)
        self.uploading = False

    def result(self):
        return ( self.Uimge.img_url,
                    self.Uimge.img_thumb_url,
                    self.Uimge.filename
                    )

class qUimge( QtGui.QMainWindow ):
    Uimge = uimge.Uimge()
    Outprint = uimge.Outprint()
    stop = False
    delimiter = r'\n'
    image_type = ('.png', '.jpe', '.jpg', '.jpeg', '.gif', '.bmp')
    def __init__(self, parent=None):
        '''docstring for __init__'''

        self.app = QtGui.QApplication(sys.argv)

        #set multilangimport locale
        import locale
        LANG = locale.getlocale()[0]
        print LANG
        if LANG:
            LANG = LANG.split('_')[0]
        else:
            LANG = 'en'
        translator = QtCore.QTranslator(self.app)

        translator.load(
                'quimge_%s.qm'%LANG,
                '/home/apkawa/Code/uimge/quimge/quimge/locale'
                ) #FIXME
        self.app.installTranslator(translator)

        #Load setting
        self.Setting = Setting()
        self.start_dir = self.Setting.get('startdir', None )
        if not self.start_dir:
            self.lastdir = self.Setting.get('lastdir', self.start_dir )
        else:
            self.lastdir = self.start_dir
        self.default_host = self.Setting.get('default_host', 'radikal.ru')
        _style = self.Setting.get('style')
        #end load setting


        QtGui.QWidget.__init__(self, parent)
        self.app.setStyle( _style)
        self.WidgetsTree = Ui_qUimge_main()
        self.WidgetsTree.setupUi( self )
        self.setWindowTitle('quimge %s'%VERSION)

        self.event_loop = QtCore.QEventLoop()

        self.clipboard = self.app.clipboard()
        self.progressBar = self.WidgetsTree.progressBar
        self.progressBar.setMinimum( 0)
        self.BoxProgress = self.WidgetsTree.BoxProgress
        self.BoxProgress.hide()

        self.upload_list = self.WidgetsTree.UploadList
        self.WidgetsTree.UploadTab.installEventFilter( self) #set key press for upload tab

        self.about_dialog = About(self)
        self.setting_dialog = qUimge_setting_dialog( self.Setting, self)

        style = self.app.style()
        self._init_SIGNALS()
        
        self.SelectHost = self.WidgetsTree.SelectHost
        make_hosts_combobox(self.SelectHost, self.default_host)

        self.WidgetsTree.ModePrint.addItem(
                "Direct url", QtCore.QVariant("Direct") )
        for k, v in self.Outprint.outprint_rules.items():
            self.WidgetsTree.ModePrint.addItem( v['desc'],
                    QtCore.QVariant( k) )
        self.WidgetsTree.Delimiter.addItem(r"\n")

    def run(self, files=None):
        '''docstring for run'''
        self.show()
        self._initFileListIcons(files)
        sys.exit( self.app.exec_() )

    def update_setting(self):
        self._set_current_host()
        #self.Setting.set('default_host', self.default_host)
        self.Setting.set('lastdir', self.lastdir)
        self.Setting.save()

    def exit(self):
        self.close()
        self.update_setting()
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

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self._add_files([u.path() for u in event.mimeData().urls()])

    def _init_SIGNALS(self):
        '''docstring for _init_SIGNALS'''
        connect = self.connect
        SIGNAL = QtCore.SIGNAL
        SLOT = QtCore.SLOT
        connect(self.WidgetsTree.action_Open,
                SIGNAL("activated()"), self._open_file)

        connect(self.WidgetsTree.actionExit,
                SIGNAL("activated()"), self.exit)
        connect(self.WidgetsTree.actionExit_2,
                SIGNAL("activated()"), self.exit)

        connect(self.WidgetsTree.actionLoad_images,
                SIGNAL("activated()"), self._open_file)
        connect(self.WidgetsTree.actionLoad_images_from_folder,
                SIGNAL("activated()"), self._open_folder)
        connect(self.WidgetsTree.actionUpload,
                SIGNAL("activated()"), self._upload)
        connect(self.WidgetsTree.actionUpload_2,
                SIGNAL("activated()"), self._upload)
        connect(self.WidgetsTree.actionClipboard,
                SIGNAL("activated()"), self._copy_to_clipboard)
        connect(self.WidgetsTree.actionAbout,
                SIGNAL("activated()"), self.about_dialog.exec_ )
        connect(self.WidgetsTree.actionPreferences,
                SIGNAL("activated()"), self.setting_dialog.exec_ )
        connect(self.WidgetsTree.actionPreferences_2,
                SIGNAL("activated()"), self.setting_dialog.exec_ )

        connect(self.WidgetsTree.StopButton,
                SIGNAL("clicked()"), self._stop_process )
        connect(self.WidgetsTree.ModePrint,
                SIGNAL("textChanged(QString)"), self._update_result)
        connect(self.WidgetsTree.Delimiter,
                SIGNAL("textChanged(QString)"), self._set_delim)
        connect(self.WidgetsTree.DeleteSelected,
                SIGNAL("clicked()"), self._clear_selected)

        connect( self.upload_list,
                SIGNAL("itemSelectionChanged()"), self._update_summary)
        connect( self.WidgetsTree.ClearUploadList,
                SIGNAL("clicked()"), self._update_summary)
        connect( self.WidgetsTree.DeleteSelected,
                SIGNAL("clicked()"), self._update_summary)

    def _initFileListIcons(self, filenames=None):
        '''
        Create File List
        '''
        self._update_summary()
        if filenames:
            self._add_files( filenames )

    def _add_file(self, fileinfo):
        '''docstring for _add_file'''
        thumb_size = 100
        max_length_filename = thumb_size/9

        path = fileinfo.filePath()
        px = QPixmap( path )
        if px.size().isNull():
            return
        filename = fileinfo.fileName()
        size = fileinfo.size()
        size_str = human( size )

        if len(filename) > max_length_filename:
            filename = '%s...%s'%(
                    filename[0:max_length_filename/2 ],
                    filename[-max_length_filename/2:],
                    )
        else:
            filename = '%s'%(
                    filename,
                    )

        text_item ="%(name)s \n [%(size)s]"%{'size': size_str, 'name':filename }

        icon = QIcon()
        icon.addPixmap( px.scaledToHeight( thumb_size )  )
        data = {
                QString('path'): path ,
                QString('size'): size,
                QString('human_size'): size_str,
                QString('fileinfo'):fileinfo,
                }
        item = QtGui.QListWidgetItem( icon, text_item, self.upload_list )
        item.setData( QtCore.Qt.UserRole,QtCore.QVariant( data ) )
        item.setToolTip( path)
        item.setSizeHint( QtCore.QSize( thumb_size+23,thumb_size+46) )

    def _add_files(self, _files):
        '''docstring for _add_files'''
        file_list = []
        for f in _files:
            f = QtCore.QFileInfo(f)
            if f.isFile():
                file_list.append(f)
            else:
                for filename in QtCore.QDir( f.absoluteFilePath() ).entryInfoList():
                    if filename.isFile():
                        file_list.append( filename )

        current_file_count = 0
        files_count = len(file_list)

        self.WidgetsTree.tabWidget.setCurrentIndex(0)

        self._stop_process(False)
        self.BoxProgress.show()
        self.progressBar.setMaximum( files_count )
        for f in file_list:
            self.progressBar.setValue( current_file_count )
            self._add_file( f)
            while self.app.processEvents():
                pass
            if self.stop:
                break
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
            size = data.get( QString('size') )
            all_size += size
            if item.isSelected():
                selected += 1
                selected_size += size
        if selected:
            status_str = unicode(
                        self.tr("Selected %s images (%s)" )
                    )%( selected, human( selected_size))
        else:
            status_str = unicode(
                    self.tr("%s images (%s)"))%( all_files, human( all_size) )

        self.WidgetsTree.statusBar.showMessage( status_str )

    def __open_file(self):#DELETEME
        '''docstring for _open_file
        Вызывается чисто Qt диалог без предпросмотра.
        '''
        _args = ( self,
                  "Select images",
                  self.lastdir,
                  "Images (*%s)" % ' *'.join([ i for i in self.image_type])
                  )
        dialog = QtGui.QFileDialog( *_args )
        dialog.setFileMode( QtGui.QFileDialog.AnyFile)
        dialog.setViewMode( QtGui.QFileDialog.Detail)
        dialog.setOption( QtGui.QFileDialog.DontUseNativeDialog, False)
        dialog.setOption( QtGui.QFileDialog.DontUseSheet, True)
        if dialog.exec_():
            filename = dialog.selectedFiles()
            print dialog.directory().path()
            self._add_files( filename)

    def _open_file(self):
        '''docstring for _open_file'''
        _args = ( self,
                  self.tr("Select images"),
                  self.lastdir,
                  unicode(
                      self.tr("Images (*%s)")) % ' *'.join(
                          [ i for i in self.image_type]
                          )
                  )
        filenames = QtGui.QFileDialog( ).getOpenFileNames( *_args )
        if filenames:
            self.lastdir = QtCore.QFileInfo( filenames[0] ).absolutePath()
            self._add_files( filenames )

    def _open_folder(self):
        '''docstring for _open_folder'''
        dialog = QtGui.QFileDialog( )
        filename = dialog.getExistingDirectory(self,
                self.tr("Select folder"),
                self.lastdir )
        if filename:
            self.lastdir = QtCore.QFileInfo( filename ).absoluteFilePath()
            self._add_files( [filename])

    def _clear_selected(self):
        '''docstring for _clear_selected'''
        items = self.upload_list.selectedItems()
        for i in items:
            it = self.upload_list.takeItem( self.upload_list.row(i))
            it = None
        self._update_summary()
        self._update_result()

    def _set_current_host( self):
        cur_h  = self.SelectHost.currentIndex()
        host, obj = self.SelectHost.itemData(cur_h).toPyObject()
        self.Uimge.set_host(obj)

    def _upload(self):
        '''docstring for _upload'''
        def preupload():
            self._stop_process(False)
            self._set_current_host()
            self.WidgetsTree.actionUpload.setEnabled(False)
            self.WidgetsTree.actionUpload_2.setEnabled(False)
            self.BoxProgress.show()
        def postupload():
            self.BoxProgress.hide()
            self.progressBar.setValue( 0 )
            self._update_result()
            self.WidgetsTree.actionUpload.setEnabled(True)
            self.WidgetsTree.actionUpload_2.setEnabled(True)
            self.WidgetsTree.tabWidget.setCurrentIndex(1)

        upload_thread = UploadThread(self)

        count = self.upload_list.count()
        self.progressBar.setMaximum( count )
        preupload()

        for i in xrange( count ):
            item = self.upload_list.item(i)
            data = item.data( QtCore.Qt.UserRole).toPyObject()
            path = data.get( QString('path') )
            upload_thread.setup( self.Uimge, unicode(path).encode("utf-8"))
            upload_thread.start()
            while upload_thread.isRunning():
                self.app.processEvents()
            data[QString('result')]= upload_thread.result()
            item.setData( QtCore.Qt.UserRole,QtCore.QVariant( data ) )
            self.progressBar.setValue( i )
            if self.stop:
                break

        postupload()

    def _update_result(self, index_or_str=None):
        '''docstring for _update_result'''
        if index_or_str:
            mp = self.WidgetsTree.ModePrint
            ci = mp.currentIndex()
            item_data = mp.itemData( ci )
            if type( index_or_str ) == QString:
                if mp.itemData(ci).isNull():
                    self.Outprint.set_rules( usr=str(index_or_str) )
                else:
                    self.Outprint.set_rules( key=str( item_data.toString()) )

        result_list =[self.upload_list.item( i)\
                        .data(QtCore.Qt.UserRole)\
                        .toPyObject()\
                        .get( QString('result') )
                        for i in xrange(self.upload_list.count())]

        _result = self.delimiter.join(
                [ self.Outprint.get_out( *r ) for r in result_list if r ]
                )
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

    def _stop_process(self, flag=True):
        '''docstring for _stop_process'''
        self.stop = flag
        pass

    def _test(self):
        def StandardIcon():
            for d in dir(QtGui.QStyle):
                if d.startswith('SP_'):
                    icon = self.app.style().standardIcon( QtGui.QStyle.__dict__[d] )
                    icon.actualSize( QtCore.QSize( 50,50) )
                    item = QtGui.QListWidgetItem( icon, d , self.upload_list)
                    item.setSizeHint( QtCore.QSize( 100+23,100+46) )
        t = UploadThread(self)
        t.setup( "Nyaaaa")
        print t.run()
        #StandardIcon()

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
