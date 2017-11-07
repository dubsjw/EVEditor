# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/forms/valueEditor.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ValueEditor(object):
    def setupUi(self, ValueEditor):
        ValueEditor.setObjectName("ValueEditor")
        ValueEditor.setWindowModality(QtCore.Qt.ApplicationModal)
        ValueEditor.resize(380, 461)
        ValueEditor.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(ValueEditor)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.veSaveButton = QtWidgets.QPushButton(ValueEditor)
        self.veSaveButton.setObjectName("veSaveButton")
        self.horizontalLayout.addWidget(self.veSaveButton)
        self.veCancelButton = QtWidgets.QPushButton(ValueEditor)
        self.veCancelButton.setObjectName("veCancelButton")
        self.horizontalLayout.addWidget(self.veCancelButton)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.veTableWidget = QtWidgets.QTableWidget(ValueEditor)
        self.veTableWidget.setColumnCount(1)
        self.veTableWidget.setObjectName("veTableWidget")
        self.veTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.veTableWidget.setHorizontalHeaderItem(0, item)
        self.veTableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.veTableWidget, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.veAddButton = QtWidgets.QPushButton(ValueEditor)
        self.veAddButton.setObjectName("veAddButton")
        self.horizontalLayout_2.addWidget(self.veAddButton)
        self.veRemoveButton = QtWidgets.QPushButton(ValueEditor)
        self.veRemoveButton.setObjectName("veRemoveButton")
        self.horizontalLayout_2.addWidget(self.veRemoveButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.retranslateUi(ValueEditor)
        QtCore.QMetaObject.connectSlotsByName(ValueEditor)

    def retranslateUi(self, ValueEditor):
        _translate = QtCore.QCoreApplication.translate
        ValueEditor.setWindowTitle(_translate("ValueEditor", "Value Editor"))
        self.veSaveButton.setText(_translate("ValueEditor", "Save"))
        self.veCancelButton.setText(_translate("ValueEditor", "Cancel"))
        item = self.veTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ValueEditor", "Value"))
        self.veAddButton.setText(_translate("ValueEditor", "Add"))
        self.veRemoveButton.setText(_translate("ValueEditor", "Remove"))

