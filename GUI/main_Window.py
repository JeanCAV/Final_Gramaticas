# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_Window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget, QLabel)

class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        if not MainMenu.objectName():
            MainMenu.setObjectName(u"MainMenu")
        MainMenu.resize(550, 500)
        MainMenu.setStyleSheet(u"/* Estilo para la ventana principal */\n"
"QWidget {\n"
"    background-color: #f0f0f0; /* Fondo gris claro */\n"
"}\n"
"\n"
"/* Estilo base para todos los QPushButton */\n"
"QPushButton {\n"
"    color: white;             /* Color de texto */\n"
"    padding: 15px;            /* Relleno interno */\n"
"    border-radius: 15px;      /* Bordes redondeados */\n"
"    border: 1px solid #555;   /* Borde sutil */\n"
"    text-align: center;         /* Alineaci\u00f3n de texto e icono */\n"

"}\n"
"\n"
"/* Estilo al pasar el mouse (hover) */\n"
"QPushButton:hover {\n"
"    background-color: #555; /* Un color gen\u00e9rico m\u00e1s oscuro */\n"
"}\n"
"\n"
"/* --- Estilos Espec\u00edficos por ID --- */\n"
"\n"
"/* Bot\u00f3n del Tren (Azul) */\n"
"#trainButton {\n"
"    background-color: #3498db; /* Azul */\n"
"    border: 1px solid #2980b9;\n"
"}\n"
"#trainButton:hover {\n"
"    background-color: #2980b9; /* Azul m\u00e1s oscuro */\n"
"}\n"
"\n"
"/* "
                        "Bot\u00f3n del Jard\u00edn (Verde) */\n"
"#gardenButton {\n"
"    background-color: #2ecc71; /* Verde */\n"
"    border: 1px solid #27ae60;\n"
"}\n"
"#gardenButton:hover {\n"
"    background-color: #27ae60; /* Verde m\u00e1s oscuro */\n"
"}\n"
"\n"
"/* Bot\u00f3n de las Mu\u00f1ecas (Rojo) */\n"
"#dollsButton {\n"
"    background-color: #e74c3c; /* Rojo */\n"
"    border: 1px solid #c0392b;\n"
"}\n"
"#dollsButton:hover {\n"
"    background-color: #c0392b; /* Rojo m\u00e1s oscuro */\n"
"}\n"
"")
        self.mainLayout = QVBoxLayout(MainMenu)
        self.mainLayout.setSpacing(25)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(50, 50, 50, 50)
        self.verticalSpacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.verticalSpacer_top)

        self.trainButton = QPushButton(MainMenu)
        self.trainButton.setObjectName(u"trainButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trainButton.sizePolicy().hasHeightForWidth())
        self.trainButton.setSizePolicy(sizePolicy)
        self.trainButton.setMinimumSize(QSize(0, 80))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.trainButton.setFont(font)
        self.trainButton.setIconSize(QSize(32, 32))
        self.trainButton.setStyleSheet("text-align: center; qproperty-iconAlignment: AlignCenter;")


        self.mainLayout.addWidget(self.trainButton)

        self.gardenButton = QPushButton(MainMenu)
        self.gardenButton.setObjectName(u"gardenButton")
        sizePolicy.setHeightForWidth(self.gardenButton.sizePolicy().hasHeightForWidth())
        self.gardenButton.setSizePolicy(sizePolicy)
        self.gardenButton.setMinimumSize(QSize(0, 80))
        self.gardenButton.setFont(font)
        self.gardenButton.setIconSize(QSize(32, 32))

        self.mainLayout.addWidget(self.gardenButton)

        self.dollsButton = QPushButton(MainMenu)
        self.dollsButton.setObjectName(u"dollsButton")
        sizePolicy.setHeightForWidth(self.dollsButton.sizePolicy().hasHeightForWidth())
        self.dollsButton.setSizePolicy(sizePolicy)
        self.dollsButton.setMinimumSize(QSize(0, 80))
        self.dollsButton.setFont(font)
        self.dollsButton.setIconSize(QSize(32, 32))

        self.mainLayout.addWidget(self.dollsButton)

        self.verticalSpacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.verticalSpacer_bottom)


        self.retranslateUi(MainMenu)

        QMetaObject.connectSlotsByName(MainMenu)
    # setupUi

    def retranslateUi(self, MainMenu):
        MainMenu.setWindowTitle(QCoreApplication.translate("MainMenu", u"Aplicaci\u00f3n Educativa", None))
        self.trainButton.setText(QCoreApplication.translate("MainMenu", u" El Tren M\u00e1gico", None))
        self.gardenButton.setText(QCoreApplication.translate("MainMenu", u" El Jard\u00edn M\u00e1gico", None))
        self.dollsButton.setText(QCoreApplication.translate("MainMenu", u" Las Mu\u00f1ecas Rusas", None))
    # retranslateUi

