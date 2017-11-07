#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Jacob Dubs"
__credits__ = ["Jacob Dubs", "Sridhar Ratnakumar"]
__version__ = "1.0.0"

# EVEditor imports
from ui_eveditor import Ui_EVEditor
from ui_valueeditor import Ui_ValueEditor
import resources

# PyQt5 imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QAbstractItemView
from PyQt5 import QtGui, QtCore

# Python imports
import sys
import os
import tempfile

# Win32 imports
from subprocess import check_call
if sys.hexversion > 0x03000000:
    import winreg
else:
    import _winreg as winreg

class Win32Environment:
    """Utility class to get/set windows environment variable"""
    
    def __init__(self, scope):
        assert scope in ('user', 'system')
        self.scope = scope
        if scope == 'user':
            self.root = winreg.HKEY_CURRENT_USER
            self.subkey = 'Environment'
        else:
            self.root = winreg.HKEY_LOCAL_MACHINE
            self.subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
            
    def getenv(self, name):
        key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_READ)
        try:
            value, _ = winreg.QueryValueEx(key, name)
        except WindowsError:
            value = ''
        return value
    
    def setenv(self, name, value):
        # Note: for 'system' scope, you must run this as Administrator
        key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
        winreg.CloseKey(key)
        # For some strange reason, calling SendMessage from the current process
        # doesn't propagate environment changes at all.
        # TODO: handle CalledProcessError (for assert)
        check_call('''"%s" -c "import win32api, win32con; \
			assert win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')"''' % sys.executable)
    
class EVEditor( QMainWindow ):
    def __init__( self ):
        super( EVEditor, self ).__init__()
        
        # Setup the ui.
        self.ui = Ui_EVEditor()
        self.ui.setupUi( self )
        
        # Connect some signals.
        self.ui.exitButton.clicked.connect( self.onExitButtonClicked )
        self.ui.actionQuit.triggered.connect( self.onExitButtonClicked )
        self.ui.saveButton.clicked.connect( self.onSaveButtonClicked )
        self.ui.addButton.clicked.connect( self.onAddButtonClicked )
        self.ui.removeButton.clicked.connect( self.onRemoveButtonClicked )
        self.ui.actionSave.triggered.connect( self.onSaveButtonClicked )
        self.ui.evTableWidget.itemDoubleClicked.connect( self.onItemDoubleClicked )
        self.ui.actionAbout.triggered.connect( self.onAboutEVEditor )
        self.ui.actionAbout_Qt.triggered.connect( self.onAboutQt )
        
        # Start calling functions
        self.SetupTableWidget()
        self.populatetable()
        
        
    def populatetable( self ):
        # Grab all of the variables.
        variables = os.environ
        length = len( variables )
        currentrow = 0
        
        #Setup the table.
        self.ui.evTableWidget.setRowCount( length )
        
        # Add environment variables to it.
        for key in variables:
            keytableitem = QTableWidgetItem()
            keytableitem.setData( QtCore.Qt.DisplayRole, key )
            
            valuetableitem = QTableWidgetItem()
            
            value = variables[key]
            valuetableitem.setData( QtCore.Qt.DisplayRole, value )
            
            # Does the value contain multiple evars?
            splitvalue = value.split( ';' )
            
            if 1 < len( splitvalue ):
                # Disable editing as we want a different editor to show on double click.
                valuetableitem.setFlags( valuetableitem.flags() & ~QtCore.Qt.ItemIsEditable )
            
            self.ui.evTableWidget.setItem( currentrow, 0, keytableitem )
            self.ui.evTableWidget.setItem( currentrow, 1, valuetableitem )
            currentrow += 1

    # Setup the table widget
    def SetupTableWidget( self ):
        # Setup the header labels.
        labels = ['Variable', 'Value']
        self.ui.evTableWidget.setHorizontalHeaderLabels( labels )
        
        # Expand the last header section.
        self.ui.evTableWidget.horizontalHeader().setStretchLastSection( True )
        
        # Set the width of the first column to be about half of the total width.
        self.ui.evTableWidget.setColumnWidth( 0, 300 )
        
    # Item has been double clicked.
    def onItemDoubleClicked( self, item ):
        flags = item.flags()
        
        # Custom edit with window because item has multiple values.
        if not flags & QtCore.Qt.ItemIsEditable:
            # Setup the dialog window.
            valueeditdialog = QDialog()
            valueeditdialog.setWindowIcon( QtGui.QIcon(':/icons/icon.png') )
            
            # Setup the ui.
            veUI = Ui_ValueEditor()
            veUI.setupUi( valueeditdialog )
            veUI.veSaveButton.clicked.connect( valueeditdialog.accept )
            veUI.veCancelButton.clicked.connect( valueeditdialog.reject )
            
            veUI.veAddButton.clicked.connect( lambda ui=veUI: self.onEVAddButtonClicked(ui) )
            
            # Populate it with the values.
            text = item.text()
            values = text.split( ';' )
            
            veUI.veTableWidget.setRowCount( len( values ) )
            currentrow = 0
            
            # Set the values in the dialog.
            for value in values:
                valueitem = QTableWidgetItem()
                valueitem.setData( QtCore.Qt.DisplayRole, value )
                
                veUI.veTableWidget.setItem( currentrow, 0, valueitem )
                currentrow += 1
            
            # Show the dialog.
            status = valueeditdialog.exec()
            
            # Test for accept or reject.
            if QDialog.Accepted == status:
                rowcount = veUI.veTableWidget.rowCount()
                evString = ''
                
                # Grab values out of the dialog.
                for i in range( 0, rowcount - 1 ):
                    evString += veUI.veTableWidget.item(i, 0).text() + ';'
                
                # Reflect the changes in the main dialog.
                item.setData( QtCore.Qt.DisplayRole, evString )

    
    def onEVAddButtonClicked( self, ui ):
        ui.evAddButton.setText( "Test" )

    # When the main about action is clicked.
    def onAboutEVEditor( self ):
        QMessageBox.about( self, "About EVEditor", "Author: Jacob Dubs\nVersion: " + __version__ + "\nEVEditor is a simple environment variable editor.\nIcon made by Freepik from www.flaticon.com. " )
        
    # When the about qt action is clicked.
    def onAboutQt( self ):
        QMessageBox.aboutQt( self, 'About Qt' )
     
    # When the add button is clicked.
    def onAddButtonClicked( self ):
        currentRowCount = self.ui.evTableWidget.rowCount()

    # Add a row.
        self.ui.evTableWidget.setRowCount( currentRowCount + 1 )

    # Create new item for the 2 columns.
        column1Item = QTableWidgetItem()
        column2Item = QTableWidgetItem()
        self.ui.evTableWidget.setItem( currentRowCount, 0, column1Item )
        self.ui.evTableWidget.setItem( currentRowCount, 1, column2Item )

    # Pre-edit the items so the user knows where to input text.
        self.ui.evTableWidget.selectRow( currentRowCount )
        self.ui.evTableWidget.editItem( column1Item )

        # Scroll to where the item has been created.
        self.ui.evTableWidget.scrollToItem( column1Item, QAbstractItemView.PositionAtCenter )

    # When the remove button is pressed.
    def onRemoveButtonClicked( self ):
        # Check to see if there is a valid selection.
        selectionModel = self.ui.evTableWidget.selectionModel()
        selectedRows = selectionModel.selectedRows()

        if( len(selectedRows) > 0 ):
            self.ui.evTableWidget.removeRow( self.ui.evTableWidget.currentRow() )

    # When the save button is clicked.
    def onSaveButtonClicked( self ):
        # Set up some variables.
        rowcount = self.ui.evTableWidget.rowCount()
        evdict = {}
        
        # Grab all of the values from the tablewidget and save them.
        for i in range( 0, rowcount ):
            evKey = self.ui.evTableWidget.item(i, 0).text()
            evValue = self.ui.evTableWidget.item(i, 1).text()
            # Save in the dictionary.
            evdict[evKey] = evValue


        for key in evdict:
            pass
        
    # When the exit button is clicked.
    def onExitButtonClicked( self ):
        sys.exit(0)
        
if __name__ == '__main__':
    #Create the application.
    app = QApplication( sys.argv )
    
    # Setup the fusion theme.
    app.setStyle( 'Fusion' )
    palette = QtGui.QPalette()
    palette.setColor( QtGui.QPalette.Window, QtGui.QColor(53,53,53) )
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    
    eveditor = EVEditor()
    eveditor.setWindowIcon(QtGui.QIcon(':/icons/icon.png'))
    eveditor.show()
    returncode = app.exec()
    sys.exit(returncode)
